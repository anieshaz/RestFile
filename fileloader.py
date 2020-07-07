import csv
from os import path
import logging

class FileLoader:

    def __init__(self, paramDict):
        self.paramDict=paramDict
    
    def __str__(self):
        return 'FileLoader->{}'.format(self.paramFile)

    def __getColumns(self):
        '''Returns the list of columns'''
        
        if path.exists(self.paramDict['filename']):
            with open(self.paramDict['filename'],mode="r") as paramVals:
                reader = csv.reader(paramVals,delimiter=self.paramDict['delimiter'])
                headers = next(reader, None)
                return headers
        else:
            logging.error("Data file {} does not exists".format(self.paramDict['filename']))
            return None


    def ddlCheck(self):
        ''' Return true if the columns defined in the parameter file exists in the data file'''

        fileColumns=self.__getColumns()
        paramColumns= [v for v in self.paramDict['outColumns']]
        if not self.paramDict['keyColumn'] in paramColumns: paramColumns.append(self.paramDict['keyColumn'])
        # If no headers exits then return false
        if fileColumns==None:
            # logging.error("Data file {} is empty".format(self.paramDict['filename']))
            return False
        # Checking if all the parameter columns exists in the file or not
        elif all(x in fileColumns for x in paramColumns):
            logging.info("Syntax check for {} passed sucessfully".format(self.paramDict['filename']))
            return True
        else:
            logging.error("DDL Check failed : Mismatch between parameter columns and the columns present in the file '{}'".format(self.paramDict['filename']))
            return False

   
    def getData(self):
        '''Extracts and returns the filtered data'''

        paramDict=self.paramDict
        mainDict=dict()
        if self.ddlCheck():
            with open(paramDict['filename'], mode="r", newline='' ) as psvfile:
                rawData = csv.DictReader(psvfile,delimiter='|') 
                for row in rawData:
                    # Filter rows on basis of filterValue passed in the parameter file
                    if not row[paramDict['keyColumn']]==paramDict['filterValue'] : continue
                    # Create the subset dictionary with the required columns for filtered data
                    mainDict[row[paramDict['keyColumn']]]={key : row[key] for key in paramDict['outColumns']}
            if mainDict=={}:
                logging.warning("No data available for filter value : {}".format(paramDict['filterValue']))
            else:
                logging.info("Data ready to be consumed")
            return mainDict
        else:
            logging.error("No data extracted from file : {}".format(self.paramDict['filename']))
            return None