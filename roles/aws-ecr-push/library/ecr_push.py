#!/usr/bin/env python3

import base64
import json
try:
    import boto3
    import botocore
    import docker
except ImportError:
    boto3 = None
    botocore = None
    docker = None

from ansible.module_utils.basic import AnsibleModule


def run(result, module):
    session = boto3.session.Session(region_name=module.params['region'])
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
    missing_repos = set(module.params['image']) - existing_repos

    for m_repo in missing_repos:
        if module.check_mode:
            repo_objects[m_repo] = None
        else:
            repo_objects[m_repo] = client.create_repository(repositoryName=m_repo)
    if missing_repos:
        result['changed'] = True
    for image, repo in repo_objects.items():
        # Now get the url and auth token
        if repo:
            auth_token = client.get_authorization_token(
                registryIds=[repo['registryId']])
            auth_token = base64.b64decode(
                auth_token['authorizationData'][0]['authorizationToken'])
            username, password = auth_token.decode('utf-8').split(':', 1)
            repo_url = repo['repositoryUri']
            if 'repos' in result:
                result['repos'][image] = repo_url
            else:
                result['repos'] = {image: repo_url}
            dc = docker.APIClient(version='auto')
            dc.login(
                username=username,
                password=password,
                registry=repo_url,
                reauth=True,
            )
            image_id = dc.images(image, quiet=True)[0]
            # Tag to the new repo
            kwa = dict(repository=repo_url)
            if module.params['tag']:
                tags = module.params['tag']
            else:
                tags = [None]
            result['push_results'] = []
            for tag in tags:
                if tag:
                    kwa['tag'] = tag
                if not module.check_mode:
                    dc.tag(image_id, **kwa)
                    push_result = dc.push(**kwa)
                    for line in push_result.splitlines():
                        this_result = json.loads(line)
                        result['push_results'].append(this_result)
                        if 'error' in this_result:
                            module.fail_json(msg=this_result['error'])
                if tag:
                    if 'tags' in result:
                        result['tags'][image].append(tag)
                    else:
                        result['tags'] = {image: [tag]}
                result['changed'] = True

    return result


def main():
    result = dict(changed=False)
    try:
        module_args = dict(
            image=dict(type='list', required=True),
            tag=dict(type='list', required=False),
            region=dict(type='str', required=False),
        )
        # TODO: add the ec2/aws args the way other ec2 modules do
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True,
        )
        if not all((boto3, botocore, docker)):
            raise Exception(
                'Requires boto3, botocore, and docker python modules.')

        module.exit_json(**run(result, module))
    except Exception as e:
        module.fail_json(msg='Failure: %s(%s)' % (type(e), str(e)), **result)


if __name__ == '__main__':
    main()
