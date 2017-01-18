import copy
import datetime
import botocore

# #############################################################################
# CONSTANTS
# #############################################################################

TASK_RUNNING = 'RUNNING'

# #############################################################################

class Task:
    def __init__(self, service, id):
        self.id = id
        self.service = service
        self.cluster = self.service.cluster
        self.ecs = self.service.ecs
        self.arn = ''
        self.containerInstanceArn = ''
        self.taskDefinitionArn = ''
        self.containers = []
        self.status = ''
        self.desiredStatus = ''
        self.version = 0
        self.startedBy = ''
        self.stoppedReason = ''
        self.createdAt = None
        self.startedAt = None
        self.stoppedAt = None
        self.group = ''
        self.initialized = False

    def initialize(self):
        try:
            response = self.ecs.describe_tasks(cluster=self.cluster.name, tasks=[self.id,])
            if len(response['tasks']) > 0:
                task = response['tasks'][0]
                self.arn = task['taskArn']
                self.containerInstanceArn = task['containerInstanceArn']
                self.status = task['lastStatus']
                self.desiredStatus = task['desiredStatus']
                self.createdAt = task['createdAt']
                self.taskDefinitionArn = task['createdAt']
                if task.has_key('version'):
                    self.version = int(task['version'])
                if task.has_key('startedBy'):
                    self.startedBy = task['startedBy']
                if task.has_key('group'):
                    self.group = task['group']
                if task.has_key('stoppedReason'):
                    self.stoppedReason = task['stoppedReason']
                if task.has_key('startedAt'):
                    self.startedAt = task['startedAt']
                if task.has_key('stoppedAt'):
                    self.stoppedAt = task['stoppedAt']
                if task.has_key('containers'):
                    self.containers = copy.deepcopy(task['containers'])
                self.initialized = True
            else:
                self.initialized = False
                raise Exception('task id not found')
        except botocore.exceptions.ClientError as e:
            self.initialized = False
            raise e

    def isInitialized(self):
        return self.initialized
