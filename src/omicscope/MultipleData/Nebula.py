import glob
import os

import pandas as pd
import seaborn as sns


class nebula:
    from .circos import circos_plot
    from .MultipleVisualization import barplot
    from .MultipleVisualization import circular_path
    from .MultipleVisualization import correlation
    from .MultipleVisualization import diff_reg
    from .MultipleVisualization import dotplot_enrichment
    from .MultipleVisualization import enrichment_overlap
    from .MultipleVisualization import fisher_heatmap
    from .MultipleVisualization import group_network
    from .MultipleVisualization import network
    from .MultipleVisualization import protein_overlap

    def __init__(self, folder, palette='Dark2', pvalue_cutoff=0.05):
        self.original_path = os.getcwd()
        self.read_omics(folder, palette=palette)
        self.group_data = []
        for o, g, l in zip(self.original, self.groups, self.labels):
            self.group_data.append(self.importing(o, g, l, pvalue_cutoff=pvalue_cutoff))

        print(f'''You imported your data successfully!
        Data description:
        1. N groups imported: {len(self.groups)}
        2. Groups: {','.join(self.groups)}
        3. N groups with enchment data: {sum(x is not None for x in self.enrichment)}
        ''')

    def read_omics(self, folder, palette):
        path = folder  # use your path
        all_files = glob.glob(path + "/*.omics")
        groups = []
        labels = []
        original = []
        enrichment = []
        for i in all_files:
            positions = []
            with open(i, 'r') as archive:
                lines = archive.readlines()
                for n, line in enumerate(lines):
                    if line == '-------\n':
                        positions.append(n)
                    if line.startswith('Experimental'):
                        groups.append(line.split('\t')[-1].split('\n')[0])
                        labels.append(line.split('\t')[-1].split('\n')[0])
                    if line.startswith('Statistics'):
                        self.pvalue = line.split('\t')[-1].split('\n')[0]
                if len(positions) == 1:
                    original.append(pd.read_csv(i, header=positions[0]+1, sep='\t'))
                    enrichment.append(None)
                else:
                    original.append(pd.read_csv(i, header=positions[0]+1, sep='\t',
                                                nrows=int((positions[1]/2)-5)))
                    enrichment.append(pd.read_csv(i, header=int((positions[1]+1)/2)+4,
                                                  sep='\t'))
                archive.close()
            self.groups = groups
            self.colors = sns.color_palette(palette, as_cmap=False, n_colors=len(groups)).as_hex()
            self.labels = labels
            self.original = original
            self.enrichment = enrichment

    def importing(self, original, group, label, pvalue_cutoff):
        df = original
        df = df[df[self.pvalue] < pvalue_cutoff][['gene_name', 'log2(fc)']].sort_values('log2(fc)', ignore_index=True)
        df['group'] = label
        df['color'] = df['log2(fc)'].round()
        return (df)

    __all__ = [
        'barplot',
        'circular_path',
        'circos_plot',
        'diff_reg',
        'dotplot_enrichment',
        'enrichment_overlap',
        'group_network',
        'network',
        'correlation',
        'overlap_stat',
        'protein_overlap'
    ]
