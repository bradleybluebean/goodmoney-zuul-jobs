Notify via Slack

Given a slack Incoming Webhook token, sends notifications, typically in a
"post" style pipeline to let users know when publishing jobs have succeeded or
failed.

**Role Variables**

.. zuul:rolevar:: slack_notify_token

   The token portion of an incoming webhook's URL (Without the
   https://hooks.slack.com/services/ prefix).

.. zuul:rolevar:: slack_notify_zuul_url

   Used to build links to the Zuul UI, i.e. "https://zuul.openstack.org".

.. zuul:rolevar:: slack_notify_channels
   :default: [omit]

   Set to a list of channels. By default this is omitted and the default
   channel for the token is used.

.. zuul:rolevar:: slack_notify_icon
   :default: https://zuul-ci.org/favicon.ico

   Used for smaller notifications.

.. zuul:rolevar:: slack_notify_emoji
   :default: omit

   Set `slack_notify_icon` to `{{ omit }}` and set this if you'd like to use an
   emoji instead of an icon URL.

.. zuul:rolevar:: slack_notify_username
   :default: Zuul

   The username field for messages from this notification.

.. zuul:rolevar:: slack_notify_success_emoji
   :default: ":thumbsup_all:"

   Appended to success messages.

.. zuul:rolevar:: slack_notify_failure_emoji
   :default: ":face_palm:"

   Appended to failure messages.
