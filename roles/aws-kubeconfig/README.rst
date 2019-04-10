This role will set up ~/.kube/config with aws-iam-authenticator. The intention
is to allow a job to use a kubernetes cluster that is backed by AWS's EKS
service.

It does not install AWS credentials for you. You will need to set that up
with the aws-credentials role first.

**Role Variables**

.. zuul:rolevar:: aws_kubectl_targets

   A list of details to set up users, clusters, and contexts in `~/.kube/config`.

   Each one consists of the following variables.

   .. zuul:rolvear:: name

      Unique name, this will be the name of the context, user, and cluster.

   .. zuul:rolevar:: kube_api_endpoint

      For each cluster, use this as the `server` field.

   .. zuul:rolevar:: kube_api_ca_data

      For each cluster, use this as the `ceritifcate-authority-data`.

   .. zuul:rolevar:: kube_api_name

      For each user, this is the name of the EKS cluster.
