import datasetmaster
import netmaster

if __name__ == '__main__':
	dataset = datasetmaster.generate()
	model = netmaster.build_model(dataset)
