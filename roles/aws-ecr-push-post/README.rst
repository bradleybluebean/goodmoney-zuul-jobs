Push docker images into ECR on post

This tags images in ECR with `zuul.build`, `zuul.pipeline`, and `zuul.newrev`,
which is useful for post commit jobs. See `aws-ecr-push` for the lower level
role used to do so.

**Role Variables**

.. zuul:rolevar:: aws_ecr_push_region

   The AWS region in which the registry resides.

.. zuul:rolevar:: aws_ecr_push_image

   Either a single string or list of strings representing the names of the
   local images to push in to ECR.

