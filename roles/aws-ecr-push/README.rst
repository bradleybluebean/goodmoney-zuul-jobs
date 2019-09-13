Push docker images into ECR

This pushes images that exist in a local docker daemon into an AWS ECR
registry. It uses configured AWS credentials according to boto's usual pattern
of loading credentials.

Assumes docker is installed.

This role will record all of the repos it has touched in a variable,
`aws_ecr_push_repos`.

**Role Variables**

.. zuul:rolevar:: aws_ecr_push_region

   The AWS region in which the registry resides.

.. zuul:rolevar:: aws_ecr_push_image

   Either a single string or list of strings representing the names of the
   local images to push in to ECR.

.. zuul:rolevar:: aws_ecr_push_tag
   :default: latest

   This is the tag to give any uploaded images.

.. zuul:rolevar:: aws_ecr_push_user
   :default: build

   User account name to use for communicating with docker.
