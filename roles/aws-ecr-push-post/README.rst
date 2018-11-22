Push docker images into ECR on post

This tags images in ECR with values from `zuul.build`, `zuul.pipeline`, and
`zuul.newrev`, or `zuul.change`, depending on the trigger type. It will prefix
each tag with the respective zuul attribute name and a '_'. So if the build is
`12345`, the pipeline is `post`, and `newrev` is `012356789abcdef`, the
specified image will be tagged `build_12345`, `pipeline_post` and
`newrev_0123456789abcdef`.

As its name implies, this is most useful for post commit jobs, though
`zuul.change` being the fallback, it can be used in a gate job as well.. See
`aws-ecr-push` for the lower level role used to do the pushing.

**Role Variables**

.. zuul:rolevar:: aws_ecr_push_region

   The AWS region in which the registry resides.

.. zuul:rolevar:: aws_ecr_push_image

   Either a single string or list of strings representing the names of the
   local images to push in to ECR.

