import time
import botocore

import cluster
import task_definition
import task

# #############################################################################
# CONSTANTS
# #############################################################################

MAX_VERIFICATIONS = 8

# #############################################################################

class Service:
    def __init__(self, cluster, name):
        self.arn = ""
        self.cluster = cluster
        self.region = self.cluster.region
        self.ecs = self.cluster.ecs
        self.initialized = False
        self.name = name
        self.status = ""
        self.desiredTaskCount = 0
        self.taskDefinition = None
        self.tasks = []

    def initialize(self):
        try:
            response = self.ecs.describe_services(cluster=self.cluster.name, services=[self.name,])
            if len(response['services']) > 0:
                service = response['services'][0]
                self.arn = service['serviceArn']
                self.status = service['status']
                self.desiredTaskCount = service['desiredCount']
                self.initialized = True
                self.getTaskDefinition()
                self.getTasks()
            else:
                self.initialized = False
                raise Exception('service name not found')
        except botocore.exceptions.ClientError as e:
            self.initialized = False
            raise e

    def isInitialized(self):
        return self.initialized

    def getTaskDefinition(self):
        try:
            if self.initialized:
                response = self.ecs.describe_services(cluster=self.cluster.name, services=[self.name,])
                if len(response['services']) > 0:
                    service = response['services'][0]
                    tdarn = service['taskDefinition']
                    self.taskDefinition = task_definition.TaskDefinition(self, tdarn)
                    self.taskDefinition.initialize()
            else:
                self.taskDefinition = None
                raise Exception('service name not found')
        except botocore.exceptions.ClientError as e:
            self.taskDefinition = None
            raise e

    def getTasks(self):
        try:
            if self.initialized:
                if len(self.tasks) > 0:
                    del self.tasks[:]
                response = self.ecs.list_tasks(cluster=self.cluster.name, serviceName=self.name)
                if len(response['taskArns']) > 0:
                    arns = response['taskArns']
                    for arn in arns:
                        tname = arn.split('/')[1].split(':')[0]
                        tobj = task.Task(self, tname)
                        tobj.initialize()
                        self.tasks.append(tobj)
            else:
                raise Exception('service not initialized')
        except botocore.exceptions.ClientError as e:
            self.tasks = []
            raise e

    def update(self):
        waiter = self.ecs.get_waiter('services_stable')
        if self.initialized:
            self.ecs.update_service(cluster=self.cluster.name, service=self.name, taskDefinition=self.taskDefinition.arn)
            waiter.wait(cluster=self.cluster.name,services=[self.name,])
        else:
            raise Exception('service not initialized')

    def rollback(self):
        waiter = self.ecs.get_waiter('services_stable')
        if self.initialized:
            response = self.ecs.list_task_definitions(familyPrefix=self.taskDefinition.family, sort='DESC')
            if len(response['taskDefinitionArns']) > 0:
                for arn in response['taskDefinitionArns']:
                    tdrev = int(arn.split('/')[1].split(':')[1])
                    if tdrev < self.taskDefinition.revision:
                        self.ecs.update_service(cluster=self.cluster.name, service=self.name, taskDefinition=arn)
                        waiter.wait(cluster=self.cluster.name,services=[self.name,])
                        self.initialize()
                        return;
                raise Exception('no task definitions eligible to rollback')
            else:
                raise Exception('not able to find a any task definition')
        else:
            raise Exception('service not initialized')
