__version__ = '1.0.1'
from typing import List
from typing import Optional

from .EnrichmentAnalysis import Enrichmentscope
from .MultipleData.Nebula import nebula
from .Omicscope import Omicscope

if __name__ != "__main__":
    print("OmicScope v " + __version__ + " For help: Insert\n" +
          "If you use  in published research, please cite: 'lallalala'\n" +
          "Reis-de-Oliveira G, Martins-de-Souza D. OmicScope: an Comprehensive Python library for Systems Biology Visualization.\n")


def OmicScope(Table: str,
              Method: str,
              ControlGroup: Optional[str] = None,
              ExperimentalDesign: str = 'static',
              pvalue: str = 'pAdjusted',
              PValue_cutoff: float = 0.05,
              FoldChange_cutoff: float = 0.0,
              logTransformed: bool = False,
              ExcludeKeratins: bool = True,
              degrees_of_freedom: int = 2,
              **kwargs) -> Omicscope:
    """OmicScope - Quantitative data

        OmicScope was specially designed taking into account the
        proteomic workflow, in which proteins are identified, quantified
        and normalized with several softwares, such as Progenesis Qi for
        Proteomics, PatternLab V and MaxQuant.

        Despite proteomic optimization, users can also input data from other
        Omics sources (e.g. Metabolomics and Transcriptomics), using
        Method = 'General'. To run this approach user need to follow the
        instructions from Input.General directory in a Excel file.

        Additionally, OmicScope also perform differential expression analysis,
        returning p-value (from t-test, Anova, and post-hoc correction),
        q-value and respective conditions Fold-Changes. If user desire to
        import the statistical analysis from other sources, the row data
        (rdata) must have a column named as "pvalue".

    Args:
        Table (str): Path to quantitative data.
        Method (str): Algorithm/software used to perform quantitative.
        ControlGroup (Optional[str], optional): Control group. Defaults to None.
        ExperimentalDesign (str, optional): Study experimental design in which
        OmicScope must take account for statistical analysis. Defaults to 'static'.
        pvalue (str, optional): Statistical parameter to take into account
        to consider entities differentially regulated. Defaults to 'pAdjusted'.
        PValue_cutoff (float, optional): Statistical cutoff. Defaults to 0.05.
        FoldChange_cutoff (float, optional): Difference cutoff. Defaults to 0.0.
        logTransformed (bool, optional): Abundance values were previously log-transformed. Defaults to False.
        ExcludeKeratins (bool, optional): Keratins proteins is excluded. Defaults to True.
        degrees_of_freedom (int, optional): Degrees of freedom used to run longitudinal analysis. Defaults to 2.

    Returns:
        OmicScope: Return a OmicScope obj. The quantitation data is stored to obj.quant_data.
    """
    omics = Omicscope(
        Table,
        Method,
        ControlGroup,
        ExperimentalDesign,
        pvalue,
        PValue_cutoff,
        FoldChange_cutoff,
        logTransformed,
        ExcludeKeratins,
        degrees_of_freedom,
        **kwargs)

    return omics


def EnrichmentScope(OmicScope: Omicscope,
                    Analysis: str = 'ORA',
                    dbs: List[str] = ['KEGG_2021_Human'],
                    padjust_cutoff: float = 0.05,
                    organism: str = 'human') -> Enrichmentscope:
    """EnrichmentScope - Enrichment Analysis

        EnrichmentScope is the module designed to perform over-representation
        and Gene-Set Enrichment Analyses of proteins and genes.

    Args:
        OmicScope (Omicscope): Omicscope object
        Analysis (str): Over-representation Analysis (ORA) or Gene-Set Enrichment Analysis (GSEA).
        Defaults to 'ORA'.
        dbs (List[str]): List of enrichment databases to perform the enrichment analysis.
        Defaults to ['KEGG_2021_Human'].
        padjust_cutoff (float, optional): statistical cutoff. Defaults to 0.05.
        organism (str, optional): Organism from which entities belong. Defaults to 'human'.

    Returns:
        Enrichmentscope: Return a EnrichmentScope obj. The results is stored to obj.results.
    """
    enrichment = Enrichmentscope(
        OmicScope,
        Analysis,
        dbs,
        padjust_cutoff,
        organism)

    return enrichment


def Nebula(folder: str,
           palette: str = 'Dark2',
           pvalue_cutoff: float = 0.05) -> nebula:
    """Nebula - Multiple group comparison

        Nebula is the module to integrate all data generated by OmicScope
        pipeline

    Args:
        folder (str): path to folder that contains all .omics files
        palette (str): Palette to assign colors and discriminate groups
        pvalue_cutoff (float): P-value threshold to consider differentially
        regulated proteins

    Returns:
        Nebula: Return a Nebula obj.
    """
    multiple_groups = nebula(folder, palette=palette, pvalue_cutoff=pvalue_cutoff)

    return multiple_groups
