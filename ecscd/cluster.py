import boto3
import botocore

import service

# #############################################################################
# CONSTANTS
# #############################################################################

DEFAULT_CLUSTER = 'default'
DEFAULT_REGION  = 'us-east-1'

# #############################################################################

class Cluster():
    def __init__(self, name=DEFAULT_CLUSTER, region=DEFAULT_REGION, key_id='', access_key=''):
        self.arn = ""
        self.initialized = False
        self.name = name
        self.region = region
        self.services = []
        self.status = ""
        try:
            if key_id == '' or access_key == '':
                self.ecs = boto3.client('ecs', region_name=region)
            else:
                self.ecs = boto3.client('ecs', region_name=region, aws_access_key_id=key_id, aws_secret_access_key=access_key)
        except botocore.exceptions.ClientError as e:
            self.ecs = None
            raise e

    def initialize(self):
        try:
            response = self.ecs.describe_clusters(clusters=[self.name,])
            if len(response['clusters']) > 0:
                cluster = response['clusters'][0]
                self.arn = cluster['clusterArn']
                self.status = cluster['status']
                self.initialized = True
                self.getServices()
            else:
                self.initialized = False
                raise Exception('cluster not found')
        except botocore.exceptions.ClientError as e:
            self.taskDefinition = None
            raise e

    def isInitialized(self):
        return self.initialized

    def getServices(self):
        try:
            if self.initialized:
                response = self.ecs.list_services(cluster=self.name)
                if len(response['serviceArns']) > 0:
                    arns = response['serviceArns']
                    for arn in arns:
                        sname = arn.split('/')[1].split(':')[0]
                        sobj = service.Service(self, sname)
                        sobj.initialize()
                        self.services.append(sobj)
            else:
                raise Exception('service not found')
        except botocore.exceptions.ClientError as e:
            self.taskDefinition = None
            raise e
