from dash import Dash, html, dcc, Input, Output, callback
import dash_bio as dashbio
from app import app
from pages.components.data_loader import load_data,genome_data,genome

path_bed = r'assets\Pk_5502transcript.bed'
gene_to_genome = genome_data(path_bed)
genome_list=genome(gene_to_genome)
path_bed = r'assets/Pk_5502transcript.bed'
def return_igv():
    return dashbio.Igv(
        id='igv-container',
        genome= genome_list,
        reference={
            'id': "Id",
            'name': "PKHN",
            'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
            'indexURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
            'order': 1000000,
            'tracks': [
                {
                    'name': 'TTAA Track',
                    'url': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
                    'indexURL': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
                    'displayMode': 'EXPANDED',
                    'nameField': 'gene',
                    'height': 150,
                    'color': 'rgb(176,141,87)'
                },
                {
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(176,141,87)'
                },
                {
                    'name': 'GTF track',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(176,141,87)'
                }
            ]
        }
    )
