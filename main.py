from flask import Flask, jsonify, abort, make_response
from params import Params
from fileloader import FileLoader
import signal
import logging
from sys import exit
from socket import gethostname

app=Flask(__name__)
logger = logging.getLogger(__name__)

log_format='%(asctime)s :: %(levelname)s :: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format,filename='rest-app.log',filemode='w')

params=Params('param.yaml')
paramsDict=params.getParams()

def makeData(params):
     '''Returns the parameter object'''

     filedata=FileLoader(params)
     return filedata

def getPort():
     '''Returns portno used by the api (default -> 5000)'''

     portno=paramsDict.get('port',5000)
     return portno

'''Error handelling'''
@app.errorhandler(400)
def bad_request(error):
     logging.error('Bad request : {}'.format(error))
     return make_response(jsonify({'error' : 'Bad request'}))

@app.errorhandler(404)
def bad_url(error):
     logging.error('Bad URL : {}\n[try http://{}:{}/api/get/<filter>]'.format(error,gethostname(),getPort()))
     return make_response(jsonify({'error' : 'Bad URL'}))

@app.errorhandler(405)
def bad_method(error):
     logging.error('Bad method : {}'.format(error))
     return make_response(jsonify({'error' : 'Bad method'}))

'''GET implementation'''
@app.route('/api/get/<filter>', methods = ['GET'])
def get_data(filter):
     paramsDict['filterValue']=filter
     data=makeData(paramsDict).getData()
     return data.get(filter,jsonify({'error':'No data found'}))

#Signal Handle
class GracefulKiller:
     kill_now = False

     def __init__(self):
          signal.signal(signal.SIGINT, self.exit_gracefully)
          signal.signal(signal.SIGTERM, self.exit_gracefully)
     
     def exit_gracefully(self,signum, frame):
          self.kill_now = True
          raise KeyboardInterrupt

'''Executes the main code here'''
if __name__=='__main__':
     if not paramsDict == None and makeData(paramsDict).ddlCheck():
          killer= GracefulKiller()
          while not killer.kill_now:
               try:
                    app.run(host=gethostname(), port=getPort())
               except OSError as e:
                    logging.error('OS Error encountered : {} : {}'.format(e.errno,e.strerror))
                    exit(0)
               except KeyboardInterrupt as e:
                    logging.error('Kill received : {} : {}'.format(e.errno,e.strerror))
                    exit(0)