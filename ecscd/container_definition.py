import copy

# #############################################################################
# CONSTANTS
# #############################################################################

DEFAULT_CONTAINER = 'default'

DEFAUlT_CPU                 = 0
DEFAULT_MEMORY              = 1024
DEFAULT_MEMORY_RESERVATION  = 512

# #############################################################################

class ContainerDefinition():
    def __init__(self, taskDefinition, name=DEFAULT_CONTAINER):
        self.taskDefinition = taskDefinition
        self.name = name
        self.ecs = self.taskDefinition.ecs
        self.image = ''
        self.cpu = DEFAUlT_CPU
        self.memory = DEFAULT_MEMORY
        self.memoryReservation = DEFAULT_MEMORY_RESERVATION
        self.essential = True
        self.hostname = ''
        self.user = ''
        self.workingDirectory = ''
        self.disableNetworking = False
        self.privileged = False
        self.readonlyRootFilesystem = False
        self.links = []
        self.portMappings = []
        self.entryPoint = []
        self.command = []
        self.environment = []
        self.mountPoints = []
        self.volumesFrom = []
        self.dnsServers = []
        self.dnsSearchDomains = []
        self.extraHosts = []
        self.dockerSecurityOptions = []
        self.ulimits = []
        self.logConfiguration = None
        self.dockerLabels = None
        self.initialized = False

    def initialize(self):
        try:
            response = self.ecs.describe_task_definition(taskDefinition=self.taskDefinition.name)
            definition = response['taskDefinition']['containerDefinitions'][0]
            self.image = definition['image']
            self.cpu = int(definition['cpu'])
            self.memory = int(definition['memory'])
            if definition.has_key('memoryReservation'):
                self.memoryReservation = int(definition['memoryReservation'])
            if definition.has_key('essential'):
                self.essential = definition['essential']
            if definition.has_key('hostname'):
                self.hostname = definition['hostname']
            if definition.has_key('user'):
                self.user = definition['user']
            if definition.has_key('workingDirectory'):
                self.workingDirectory = definition['workingDirectory']
            if definition.has_key('disableNetworking'):
                self.disableNetworking = bool(definition['disableNetworking'])
            if definition.has_key('privileged'):
                self.privileged = bool(definition['privileged'])
            if definition.has_key('readonlyRootFilesystem'):
                self.readonlyRootFilesystem = bool(definition['readonlyRootFilesystem'])
            if definition.has_key('links'):
                self.links = copy.copy(definition['links'])
            if definition.has_key('entryPoint'):
                self.entryPoint = copy.copy(definition['entryPoint'])
            if definition.has_key('command'):
                self.command = copy.copy(definition['command'])
            if definition.has_key('portMappings'):
                self.portMappings = copy.deepcopy(definition['portMappings'])
            if definition.has_key('environment'):
                self.environment = copy.deepcopy(definition['environment'])
            if definition.has_key('mountPoints'):
                self.mountPoints = copy.deepcopy(definition['mountPoints'])
            if definition.has_key('volumesFrom'):
                self.volumesFrom = copy.deepcopy(definition['volumesFrom'])
            if definition.has_key('dnsServers'):
                self.dnsServers = copy.copy(definition['dnsServers'])
            if definition.has_key('dnsSearchDomains'):
                self.dnsSearchDomains = copy.copy(definition['dnsSearchDomains'])
            if definition.has_key('extraHosts'):
                self.extraHosts = copy.deepcopy(definition['extraHosts'])
            if definition.has_key('dockerSecurityOptions'):
                self.dockerSecurityOptions = copy.copy(definition['dockerSecurityOptions'])
            if definition.has_key('dockerLabels'):
                self.dockerLabels = copy.copy(definition['dockerLabels'])
            if definition.has_key('ulimits'):
                self.ulimits = copy.deepcopy(definition['ulimits'])
            if definition.has_key('logConfiguration'):
                self.logConfiguration = copy.deepcopy(definition['logConfiguration'])
            self.initialized = True
        except:
            self.initialized = False
            raise Exception('not able to initialize container definition')

    def isInitialized(self):
        return self.initialized

    def to_dict(self):
        if self.initialized:
            d = dict()
            d['name'] = self.name
            d['image'] = self.image
            d['cpu'] = self.cpu
            d['memory'] = self.memory
            d['memoryReservation'] = self.memoryReservation
            d['essential'] = self.essential
            d['disableNetworking'] = self.disableNetworking
            d['privileged'] = self.privileged
            d['readonlyRootFilesystem'] = self.readonlyRootFilesystem
            if self.user != '':
                d['user'] = self.user
            if self.workingDirectory != '':
                d['workingDirectory'] = self.workingDirectory
            if self.hostname != '':
                d['hostname'] = self.hostname
            if len(self.links) > 0:
                d['links'] = copy.copy(self.links)
            if len(self.portMappings) > 0:
                d['portMappings'] = copy.deepcopy(self.portMappings)
            if len(self.entryPoint) > 0:
                d['entryPoint'] = copy.copy(self.entryPoint)
            if len(self.command) > 0:
                d['command'] = copy.copy(self.command)
            if len(self.environment) > 0:
                d['environment'] = copy.deepcopy(self.environment)
            if len(self.mountPoints) > 0:
                d['mountPoints'] = copy.deepcopy(self.mountPoints)
            if len(self.volumesFrom) > 0:
                d['volumesFrom'] = copy.deepcopy(self.volumesFrom)
            if len(self.dnsServers) > 0:
                d['dnsServers'] = copy.copy(self.dnsServers)
            if len(self.dnsSearchDomains) > 0:
                d['dnsSearchDomains'] = copy.copy(self.dnsSearchDomains)
            if len(self.extraHosts) > 0:
                d['extraHosts'] = copy.deepcopy(self.extraHosts)
            if len(self.dockerSecurityOptions) > 0:
                d['dockerSecurityOptions'] = copy.copy(self.dockerSecurityOptions)
            if len(self.ulimits) > 0:
                d['ulimits'] = copy.deepcopy(self.ulimits)
            if self.dockerLabels != None:
                d['dockerLabels'] = copy.deepcopy(self.dockerLabels)
            if self.logConfiguration != None:
                d['logConfiguration'] = copy.deepcopy(self.logConfiguration)
            return d
        else:
            return None
