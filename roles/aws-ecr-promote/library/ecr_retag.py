#!/usr/bin/env python3

try:
    import boto3
    import botocore
    import requests
except ImportError:
    boto3 = None
    botocore = None
    requests = None

import base64

from ansible.module_utils.basic import AnsibleModule


def run(result, module):
    session = boto3.session.Session(
        region_name=module.params['region'],
        profile_name=module.params['profile'],
    )
    client = session.client('ecr')
    existing_repos = set()
    repo_objects = {}
    for image in module.params['image']:
        # Create any that don't exist
        for page in client.get_paginator('describe_repositories').paginate():
            for repo in page['repositories']:
                if repo['repositoryName'] == image:
                    repo_objects[image] = repo
                    existing_repos.add(repo['repositoryName'])
    missing_repos = list(set(module.params['image']) - existing_repos)
    if missing_repos:
        result['missing_repos'] = missing_repos
    missing_tags = []
    failures = []
    result['results'] = []

    session = requests.Session()

    for image, repo in repo_objects.items():
        # Now get the url and auth token
        if repo:
            token = client.get_authorization_token(
                registryIds=[repo['registryId']])
            token = base64.b64decode(
                token['authorizationData'][0]['authorizationToken'])
            (user, password) = token.decode('ascii').split(':', 2)
            auth = (user, password)
            repo_url = "https://{}".format(repo['repositoryUri'])
            if repo_url.startswith('https://'):
                image_ref = repo_url.split('https://')[1]
            else:
                image_ref = repo_url
            if 'repos' in result:
                result['repos'][image] = image_ref
            else:
                result['repos'] = {image: image_ref}
            # The url is the pull URI, but we want the base registry URI so we
            # can talk to the registry v2 API
            repo_url = repo_url.rsplit('/', 1)[0]
            # Fetch manifest for from token
            from_tag = module.params['from']
            manifest = session.get("{uri}/v2/{image}/manifests/{tag}".format(
                uri=repo_url, image=image, tag=from_tag), auth=auth)
            if manifest.status_code == 404:
                missing_tags.append(dict(image=image, tag=from_tag))
                continue
            if not manifest.ok:
                failures.append(
                    dict(image=image,
                         tag=from_tag,
                         reason=manifest.reason,
                         text=manifest.text,
                         headers=manifest.request.headers))
                continue

            headers = {"content-type": manifest.headers["content-type"]}
            for tag in module.params['to']:
                if not module.check_mode:
                    p_result = session.put(
                        "{uri}/v2/{image}/manifests/{tag}".format(
                            uri=repo_url, image=image, tag=tag),
                        data=manifest.text, headers=headers, auth=auth)
                    if not p_result.ok:
                        failures.append(
                            dict(image=image,
                                 tag=tag,
                                 reason=p_result.reason,
                                 text=p_result.text,
                                 headers=p_result.headers))
                    else:
                        result['results'].append(
                            dict(image=image, tag=tag, reason=p_result.reason))
                else:
                    result['results'].append(
                        dict(image=image, tag=tag))
                result['changed'] = True

    if missing_tags:
        result['missing_tags'] = missing_tags
    if failures:
        result['failures'] = failures
    if missing_tags or missing_repos or failures:
        raise RuntimeError("Not all actions could be completed")

    return result


def main():
    result = dict(changed=False)
    try:
        module_args = dict(
            image=dict(type='list', required=True),
            to=dict(type='list', required=True),
            region=dict(type='str', required=False),
            profile=dict(type='str', required=False),
        )
        module_args['from'] = dict(type='str', required=True)
        # TODO: add the ec2/aws args the way other ec2 modules do
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True,
        )
        if not all((boto3, botocore, requests)):
            raise Exception(
                'Requires boto3, botocore, and requests python modules.')

        module.exit_json(**run(result, module))
    except Exception as e:
        module.fail_json(msg='Failure: %s(%s)' % (type(e), str(e)), **result)


if __name__ == '__main__':
    main()
