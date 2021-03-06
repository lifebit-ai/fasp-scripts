#  IMPORTS
import sys 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import bdcDRSClient
from fasp.workflow import GCPLSsamtools
from fasp.search import BigQuerySearchClient

def main(argv):


	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()
# 	query = """
#      	SELECT subject_id, read_drs_id
#      	FROM `isbcgc-216220.COPDGene.phenotype_drs`
#      	where weight_kg between 91.8 and 93.0
#      	LIMIT 1"""
	query = """
		SELECT submitter_id, read_drs_id
		FROM `isbcgc-216220.onek_genomes.ssd_drs`
		where population = 'BEB'
		LIMIT 1"""

	# BioDataCatalyst
	drsClient = bdcDRSClient('~/.keys/bdc_credentials.json', 'gs')
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'])

	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery(query, 'One k  query ')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
