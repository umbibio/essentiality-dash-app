import pandas as pd

def load_data(path):
  d = pd.read_excel(path)
  df= pd.DataFrame(d)
  return df

path_bed = r'assets/Pk_5502transcript.bed'
def genome_data(path_bed):
   bed_data = pd.read_csv(path_bed, sep='\s+', header=None, names=['chrom', 'start', 'end', 'gene_name','dot', 'strand'])
   gene_to_genome = {row['gene_name']: row['chrom'] for index, row in bed_data.iterrows()}
   return gene_to_genome

def genome(gene_to_genome):
   genome_list = {}
   genome_list = list(gene_to_genome.values())
   return genome_list