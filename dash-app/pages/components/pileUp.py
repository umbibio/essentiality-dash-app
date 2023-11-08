# from dash import html, dcc
# import dash_bio as dashbio
# from app import app
# from pages.components.data_loader import locus_data

# def return_pileup():
#     return dashbio.Pileup(
#         id='pileup-container',
#         reference=[
#             {
#                 'name': 'PKNH_14_v2',
#                 'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
#                 'faiURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
#             },
#             ],
#         tracks=[
#             {
#                 'name': 'TTAA Track',
#                 'alignmentFile': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
#                 'alignmentIndex': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
#                 'height': 150,
#                 'color': 'rgb(176, 141, 87)'
#             },
#             {
#                 'name': 'TTAA Genome Pos',
#                 'trackType': 'FeatureTrack',
#                 'sourceType': 'bed',
#                 'source': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
#                 'height': 100,
#                 'color': 'rgb(176, 141, 87)'
#             },
#             {
#                 'name': 'GTF track',
#                 'trackType': 'GeneTrack',
#                 'sourceType': 'gtf',
#                 'source': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
#                 'height': 100,
#                 'color': 'rgb(176, 141, 87)'
#             }
#         ]
#     )

# def print_asset_urls():
#     # Define the asset filenames
#     genome_fasta = 'PlasmoDB-58_PknowlesiH_Genome.fasta'
#     genome_fai = 'PlasmoDB-58_PknowlesiH_Genome.fasta.fai'
#     ttaa_bam = '75Pk_20231022_TTAA.sorted.bam'
#     ttaa_bai = '75Pk_20231022_TTAA.sorted.bai'
#     ttaa_bed = 'Pk_theo_TTAA__include_contigs_R_modified_final2.bed'
#     gtf = 'PlasmoDB-58_PknowlesiH.gtf'

#     # Print the asset URLs
#     print("Genome Fasta URL:", app.get_asset_url(genome_fasta))
#     print("Genome Fai URL:", app.get_asset_url(genome_fai))
#     print("TTAA BAM URL:", app.get_asset_url(ttaa_bam))
#     print("TTAA BAI URL:", app.get_asset_url(ttaa_bai))
#     print("TTAA BED URL:", app.get_asset_url(ttaa_bed))
#     print("GTF URL:", app.get_asset_url(gtf))
# print_asset_urls()
from dash import html, dcc
import dash_bio as dashbio
from app import app


def return_pileup():
    # tracks = [
    #     {
    #         'name': 'TTAA Track',
    #         'alignmentFile': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
    #         'alignmentIndex': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
    #         'height': 150,
    #         'color': 'rgb(176, 141, 87)'
    #     },
        # {
        #     'name': 'TTAA Genome Pos',
        #     'trackType': 'FeatureTrack',
        #     'sourceType': 'bed',
        #     'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
        #     'height': 100,
        #     'color': 'rgb(176, 141, 87)'
        # },
        # {
        #     'name': 'GTF track',
        #     'trackType': 'GeneTrack',
        #     'sourceType': 'gtf',
        #     'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
        #     'height': 100,
        #     'color': 'rgb(176, 141, 87)'
        # }
    # ]

    # Check if all track URLs are specified
    # for track in tracks:
    #     if not all(key in track for key in ('alignmentFile', 'alignmentIndex')):
    #         print(f"Error: Missing URL in track - {track['name']}")
    #         return None  # Return None to indicate an error

    # Continue creating the Pileup component
    return dashbio.Pileup(
        id='pileup-container',
        reference=[
            {
                'name': 'PKNH_14_v2',
                'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
                'faiURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
            },
        ],
        # tracks=tracks
    )

bed_url = app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed')
print("BED URL:", bed_url)