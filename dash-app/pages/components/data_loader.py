import pandas as pd

def load_data(path):
  """
    Load data from an Excel file and return it as a DataFrame.

    :param path: Path to the Excel file.
    :return: Pandas DataFrame containing the data.
    """
  d = pd.read_excel(path)
  df= pd.DataFrame(d)
  return df

path_bed = r'assets/Pk_5502transcript_modified.bed'
def genome_data(path_bed):
   """
    Read bed data from a file and create a mapping of gene names to genomic coordinates.

    :param path_bed: Path to the BED file containing genomic information.
    :return: Dictionary mapping gene names to genomic coordinates.
    """
   bed_data = pd.read_csv(path_bed, sep='\s+', header=None, names=['chrom', 'start', 'end', 'gene_name','dot', 'strand'])
   gene_to_genome = {row['gene_name']: f"{row['chrom']}:{row['start']}-{row['end']}" for index, row in bed_data.iterrows()}
   return gene_to_genome

def genome(gene_to_genome):
   """
    Extract genomic coordinates from a gene-to-genome mapping.

    :param gene_to_genome: Dictionary mapping gene names to genomic coordinates.
    :return: List of genomic coordinates.
    """
   genome_list = {}
   genome_list = list(gene_to_genome.values())
   return genome_list