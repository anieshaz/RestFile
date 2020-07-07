import yaml
# import os.path
from os import path
import logging

class Params:
    
    def __init__(self,paramFile):
        self.paramFile=paramFile
    
    def __str__(self):
        return 'Params->{}'.format(self.paramFile)
    
    def __getParams(self):
        '''Return the parameters in dictionary structure'''
        
        paramDict=dict()
        try:
            if path.exists(self.paramFile):
                with open(self.paramFile,mode="r") as paramFile:
                    paramDict = yaml.load(paramFile, Loader=yaml.FullLoader)
                    return paramDict
        except FileNotFoundError:
            logging.error("Parameter file {} doesnt exists".format(self.paramFile))
            return None

    def __sanityCheck(self):
        ''' Validates the required keys to extract data from 
        the data file are present in the parameter file'''

        keys=['outColumns','filename','keyColumn','delimiter']
        paramDict=self.__getParams()
        isValid=False
        # isValid is set to False if the required parameters are not defined
        for k in keys:
            if  paramDict == None:
                isValid= False
                logging.error("Parameter file {} not found".format(self.paramFile))
                break
            elif k in paramDict.keys():
                isValid= True
            else:
                isValid= False
                logging.error("Parameter file should have {} defined".format(keys))
                break
        if isValid: logging.info("Parameter file {} read successfully".format(self.paramFile))
        return isValid
    
    def getParams(self):
        if self.__sanityCheck():
            logging.info("Fetching Parameters from {}".format(self.paramFile))
            return self.__getParams()