from . import datasetmaster
from . import netmaster
from .netmaster import binary_predictor
from . import log


def build():
	dataset = datasetmaster.generate()
	netmaster.build_model(dataset)

if __name__=='__main__':
	build()
