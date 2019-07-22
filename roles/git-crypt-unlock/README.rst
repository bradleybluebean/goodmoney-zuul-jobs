Unlock a git-crypt encrypted working copy

Takes a base64 encoded exported key as a variable and uses it to unlock
a repo that has been encrypted with `git-crypt`_.

**Role Variables**

.. zuul:rolevar:: git_crypt_key

   The secret key that will be used to unlock the repo. Must be a base64
   encoded ascii string.

.. zuul:rolevar:: git_crypt_key_name
   :default: ""

   A string representing the name of the git-crypt key with which to unlock the
   repo. If left blank, the default git-crypt key is used.

.. zuul:rolevar:: git_crypt_repo
   :default: {{ zuul.project.src_dir }}

   Path to working copy that will be unlocked with `git-crypt`_.

.. zuul:rolevar:: git_crypt_keystorage
   :default: /mnt/keystorage

   Where to mount a ramdisk to temporarily store the `git-crypt`_ key.
