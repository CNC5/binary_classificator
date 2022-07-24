import datasetmaster
import netmaster
from netmaster import binary_predictor
import log


def build():
	dataset = datasetmaster.generate()
	netmaster.build_model(dataset)

if __name__=='__main__':
	build()