Promote tagged images in AWS ECR

This looks for the appropriate tag, change_###, and adds the pipeline_XXX tag
to the same image.  The intended use case is to run in a change-aware
post-merge pipeline, generally called "promote". This allows reusing
gate-built-and-tested images once the commit has landed.

**Role Variables**

.. zuul:rolevar:: aws_ecr_promote_region

   The AWS region in which the registry resides.

.. zuul:rolevar:: aws_ecr_promote_image

   Either a single string or list of strings representing the names of the
   local images to retag.

.. zuul:rolevar:: aws_ecr_push_user
   :default: build

   User account name to become - should be the user who has AWS credentials
   already configured.
