ECSCD
=======================

A package to provide a command line application and a simple library to manage
the deploy of a docker image that was already uploaded to an ECS repository and
needs to be deployed to an ECS cluster.

----

Once you have the base skeleton of your ECS service defined you can use the
*ecscd* command to deploy a new container image whenever you push it to your
repository or attach it in your continuous delivery process to be called
automatically by softwares as Rundeck, Jenkins, etc. The base AWS EC2 Container
Service requirements are:

1. A container image repository created and containing your latest image;
2. A task definition with proper container settings;
3. An ECS cluster with EC2 instances attached (you may use the default cluster);
4. A service defined in the cluster where the container image will be run;

The process in which I use *ecscd* is the following:

1. Code is deployed to Github;
2. Travis.ci is activated to run the test suite;
3. Once Travis.ci successfully test the code it builds a new container image;
4. Travis.ci pushes the image to AWS repository;
5. Travis.ci calls Rundeck API asking it to run the deploy job;
6. Rundeck then runs the job that will run *ecscd* to deploy the new image;

Sure, if you are versed in AWS api you can make Travis.ci directly do what
*ecscd* is doing, however, if you manage multiple applications and you have a
diverse team with different responsibilities there will come the time when one
will need to define a proper standard for the deploy and a center point of
management for the DevOps teams to use. Having this in mind is the purpose why
I have built this application and shared it with the community.

If you are new to EC2 Container Service I strongly recommend you to read about
it in here_.

Hope you enjoy it!

.. _here: https://aws.amazon.com/ecs/
