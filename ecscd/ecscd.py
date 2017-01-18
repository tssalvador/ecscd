#!/usr/bin/env python

import sys
import getopt
import botocore
import os.path
import ConfigParser

from cluster import Cluster, DEFAULT_CLUSTER, DEFAULT_REGION

# #############################################################################
# DEFAULTS
# #############################################################################

DEFAULT_PROGNAME    = 'ecscd'
DEFAULT_CONFIG_FILE = [
    './.ecscd.cfg',
    '%s/.ecscd.cfg' % os.path.expanduser("~"),
    '/etc/ecscd.cfg']

# #############################################################################
# CONSTANTS
# #############################################################################

EXIT_ERROR      = 1
EXIT_SUCCESS    = 0
ACTION_DEPLOY    = 'deploy'
ACTION_ROLLBACK  = 'rollback'
SHORT_OPTS      = "c:d:hr:"
LONG_OPTS       = ["config=", "deploy=", "help", "rollbak="]

# #############################################################################
# FUNCTIONS
# #############################################################################

def usage():
    print "deploy:"
    print "\t%s [-c path] -d application" % DEFAULT_PROGNAME
    print ""
    print "rollback:"
    print "\t%s [-c path] -r application" % DEFAULT_PROGNAME
    print ""
    print "parameters:"
    print "\t-c, --config [configuration file]"
    print "\t-d, --deploy [application name]"
    print "\t-h, --help"
    print "\t-r, --rollback [application name]"
    print ""

# #############################################################################

def main():
    appName = ''
    serviceName = ''
    access_key = ''
    key_id = ''
    clusterName = DEFAULT_CLUSTER
    configFile = ''
    region = DEFAULT_REGION
    action = ACTION_DEPLOY

    try:
        opts, args = getopt.getopt(sys.argv[1:], SHORT_OPTS, LONG_OPTS)
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(EXIT_ERROR)

    for o, a in opts:
        if o in ("-c", "--config"):
            configFile = a
            print "setting config file path to '%s'" % configFile
        elif o in ("-d", "--deploy"):
            appName = a
            action = ACTION_DEPLOY
            print "deploying application '%s'" % appName
        elif o in ("-h", "--help"):
            usage()
            sys.exit(EXIT_SUCCESS)
        elif o in ("-r", "--rollback"):
            appName = a
            action = ACTION_ROLLBACK
            print "rolling back application '%s'" % appName
        else:
            print "unkown option '%s'" % o
            sys.exit(EXIT_ERROR)

    if configFile == '':
        try:
            for f in DEFAULT_CONFIG_FILE:
                if os.path.exists(f) or os.path.islink(f):
                    configFile = f
                    break
                if f == DEFAULT_CONFIG_FILE[-1]:
                    raise
        except:
            print 'error: config file not found'
            sys.exit(EXIT_ERROR)

    try:
        print "using config file '%s'" % configFile
        parser = ConfigParser.SafeConfigParser()
        parser.read(configFile)
    except ConfigParser.ParsingError as err:
        print 'fatal: error parsing configuration file'
        sys.exit(EXIT_ERROR)

    if not parser.has_section(appName):
        print "fatal: configuration not found for application '%s'" % appName
        sys.exit(EXIT_ERROR)

    if  parser.has_option(appName, 'region'):
        region = parser.get(appName, 'region')

    if parser.has_option(appName, 'cluster'):
        clusterName = parser.get(appName, 'cluster')

    if parser.has_option(appName, 'aws_access_key_id'):
        key_id = parser.get(appName, 'aws_access_key_id')

    if parser.has_option(appName, 'aws_secret_access_key'):
        access_key = parser.get(appName, 'aws_secret_access_key')

    if  parser.has_option(appName, 'service'):
        serviceName = parser.get(appName, 'service')
    else:
        print "fatal: service name option not found for application '%s'" % appName
        sys.exit(EXIT_ERROR)

    print "using region '%s'" % region
    print "using cluster '%s'" % clusterName
    print "using service '%s'" % serviceName

    try:
        print 'cluster being initialized...'
        cluster = Cluster(name=clusterName, region=region, key_id=key_id, access_key=access_key)
        cluster.initialize()

        if cluster.isInitialized():
            print 'cluster initialized'
        else:
            print 'fatal: cluster could not be initialized'
            sys.exit(EXIT_ERROR)

        for service in cluster.services:
            if service.name == serviceName:
                if action == ACTION_DEPLOY:
                    print 'starting deploy process for "%s" application' % appName
                    print 'current task definition is "%s:%d"' % (service.taskDefinition.name, service.taskDefinition.revision)
                    service.taskDefinition.register()
                    print 'new task definition "%s:%d" registered' % (service.taskDefinition.name, service.taskDefinition.revision)
                    print 'deploying...'
                    service.update()
                    print 'application deployed successfully'
                else:
                    print 'starting rollback process for "%s" application' % appName
                    print 'current task definition is "%s:%d"' % (service.taskDefinition.name, service.taskDefinition.revision)
                    print 'rolling back...'
                    service.rollback()
                    print 'application rollback completed successfully to revsion "%s:%d"' % (service.taskDefinition.name, service.taskDefinition.revision)
    except botocore.exceptions.ClientError as e:
        print 'fatal: %s' % str(e)
        sys.exit(EXIT_ERROR)
    except Exception as e:
        print 'fatal: %s' % str(e)
        sys.exit(EXIT_ERROR)

    sys.exit(EXIT_SUCCESS)

# #############################################################################

if __name__ == "__main__":
    main()
    sys.exit(EXIT_SUCCESS)
