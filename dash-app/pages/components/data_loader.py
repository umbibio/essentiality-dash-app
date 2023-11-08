import pandas as pd

path = r'assets/MIS_OIS_BM.xlsx'
def load_data(path):
  d = pd.read_excel(path)
  df= pd.DataFrame(d)
  return df

# path_bed = r'D:\Demo_App\dash-app\assets\Pk_5502transcript.bed'
# def locus_data(path_bed):
#     bed_data = pd.read_csv(path_bed, sep='\t', header=None, names=['chrom', 'start', 'end', 'gene_name', 'strand'])
#     gene_to_region = {row['gene_name']: f'{row["chrom"]}:{row["start"]}-{row["end"]}' for index, row in bed_data.iterrows()}
#     return gene_to_region