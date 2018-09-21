This role will set up kubectl with aws-iam-authenticator. The intention
is to allow a job to use a kubernetes cluster that is backed by AWS's
IAM authentication plugins.

It does not install AWS credentiasl for you. You will need to set that up
with the aws-credentials role first.
