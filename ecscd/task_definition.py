import copy
import botocore

import container_definition

# #############################################################################
# CONSTANTS
# #############################################################################

DEFAULT_NETWORK_MODE = 'bridge'

NETWORK_BRIDGE  = 'bridge'
NETWORK_HOST    = 'host'
NETWORK_NONE    = 'none'

TASK_DEFINITION_STATUS_ACTIVE   = 'ACTIVE'
TASK_DEFINITION_STATUS_INACTIVE = 'INACTIVE'

# #############################################################################

class TaskDefinition:
    def __init__(self, service, arn):
        self.name = arn.split('/')[1].split(':')[0]
        self.service = service
        self.region = self.service.region
        self.ecs = self.service.ecs
        self.arn = arn
        self.containerDefinition = None
        self.family = ''
        self.taskRoleArn = ''
        self.networkMode = DEFAULT_NETWORK_MODE
        self.revision = arn.split('/')[1].split(':')[1]
        self.volumes = []
        self.status = TASK_DEFINITION_STATUS_INACTIVE
        self.requiresAttributes = []
        self.requiresAttributes = []
        self.initialized = False

    def initialize(self):
        try:
            response = self.ecs.describe_task_definition(taskDefinition=self.arn)
            definition = response['taskDefinition']
            self.arn = definition['taskDefinitionArn']
            self.family = definition['family']
            self.status = definition['status']
            self.revision = int(definition['revision'])
            self.networkMode = definition['networkMode']
            if definition.has_key('taskRoleArn'):
                self.taskRoleArn = definition['taskRoleArn']
            if definition.has_key('volumes'):
                self.volumes = copy.deepcopy(definition['volumes'])
            if definition.has_key('requiresAttributes'):
                self.requiresAttributes = copy.deepcopy(definition['requiresAttributes'])
            self.initialized = True
            self.getContainerDefinition()
        except botocore.exceptions.ClientError as e:
            self.initialized = False
            raise e

    def isInitialized(self):
        return self.initialized

    def getContainerDefinition(self):
        try:
            if self.initialized:
                response = self.ecs.describe_task_definition(taskDefinition=self.name)
                if len(response['taskDefinition']['containerDefinitions']) > 0:
                    cdef = response['taskDefinition']['containerDefinitions'][0]
                    cdefname = cdef['name']
                    self.containerDefinition = container_definition.ContainerDefinition(self, cdefname)
                    self.containerDefinition.initialize()
            else:
                self.containerDefinition = None
                raise errors.InitalizationError('task definition not initialized')
        except botocore.exceptions.ClientError as e:
            self.containerDefinition = None
            raise e

    def register(self):
        try:
            if self.initialized:
                response = self.ecs.register_task_definition(family=self.family, taskRoleArn=self.taskRoleArn, networkMode=self.networkMode, containerDefinitions=[self.containerDefinition.to_dict(),], volumes=self.volumes)
                if response['taskDefinition'] != '':
                    definition = response['taskDefinition']
                    self.arn = definition['taskDefinitionArn']
                    self.initialize()
                else:
                    raise Exception('failed registering task definition ')
            else:
                raise Exception('task definition not initialized')
        except botocore.exceptions.ClientError as e:
            raise e
