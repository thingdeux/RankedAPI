# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.
"""
A BitBucket Builds template for deploying an application revision to AWS CodeDeploy
narshiva@amazon.com
v1.0.0
"""
from __future__ import print_function
import os
import sys
from time import strftime
import boto3
from botocore.exceptions import ClientError

VERSION_LABEL = strftime("%Y%m%d%H%M%S")
CURRENT_ENVIRONMENT = "dev"

def get_environment_variable(name):
    ENVIRONMENT_VARIABLE_KEYS = {
        "dev": {
            "APPLICATION_NAME": str(os.getenv('APPLICATION_NAME')),
            "DEPLOYMENT_GROUP_NAME": str(os.getenv('DEPLOYMENT_GROUP_NAME')),
            "S3_BUCKET": str(os.getenv('S3_BUCKET')),
            "DEPLOYMENT_CONFIG": str(os.getenv('DEPLOYMENT_CONFIG')),
            "BUCKET_KEY": "{}/{}-bitbucket_builds.zip".format(str(os.getenv('APPLICATION_NAME')), VERSION_LABEL)
        },
        "demo": {
            "APPLICATION_NAME": str(os.getenv('DEMO_APPLICATION_NAME')),
            "DEPLOYMENT_GROUP_NAME": str(os.getenv('DEMO_DEPLOYMENT_GROUP_NAME')),
            "S3_BUCKET": str(os.getenv('DEMO_S3_BUCKET')),
            "DEPLOYMENT_CONFIG": str(os.getenv('DEPLOYMENT_CONFIG')),
            "BUCKET_KEY": "{}/{}-bitbucket_builds.zip".format(str(os.getenv('DEMO_APPLICATION_NAME')), VERSION_LABEL)
        }
    }
    return ENVIRONMENT_VARIABLE_KEYS[CURRENT_ENVIRONMENT][name]

def upload_to_s3(artifact):
    """
    Uploads an artifact to Amazon S3
    """
    try:
        client = boto3.client('s3')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False
    try:
        client.put_object(
            Body=open(artifact, 'rb'),
            Bucket=get_environment_variable('S3_BUCKET'),
            Key=get_environment_variable('BUCKET_KEY')
        )
    except ClientError as err:
        print("Failed to upload artifact to S3.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access artifact.zip in this directory.\n" + str(err))
        return False
    return True


def deploy_new_revision():
    """
    Deploy a new application revision to AWS CodeDeploy Deployment Group
    """
    try:
        client = boto3.client('codedeploy')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        response = client.create_deployment(
            applicationName=get_environment_variable('APPLICATION_NAME'),
            deploymentGroupName=get_environment_variable('DEPLOYMENT_GROUP_NAME'),
            revision={
                'revisionType': 'S3',
                's3Location': {
                    'bucket': get_environment_variable('S3_BUCKET'),
                    'key': get_environment_variable('BUCKET_KEY'),
                    'bundleType': 'zip'
                }
            },
            deploymentConfigName=get_environment_variable('DEPLOYMENT_CONFIG'),
            description='New deployment from BitBucket',
            ignoreApplicationStopFailures=True
        )
    except ClientError as err:
        print("Failed to deploy application revision.\n" + str(err))
        return False

    """
    Wait for deployment to complete
    """
    while 1:
        try:
            deploymentResponse = client.get_deployment(
                deploymentId=str(response['deploymentId'])
            )
            deploymentStatus = deploymentResponse['deploymentInfo']['status']
            if deploymentStatus == 'Succeeded':
                print("Deployment Succeeded")
                return True
            elif (deploymentStatus == 'Failed') or (deploymentStatus == 'Stopped'):
                print("Deployment Failed")
                return False
            elif (deploymentStatus == 'InProgress') or (deploymentStatus == 'Queued') or (
                deploymentStatus == 'Created'):
                continue
        except ClientError as err:
            print("Failed to deploy application revision.\n" + str(err))
            return False
    return True


def main():
    # Current Options - dev|demo
    CURRENT_ENVIRONMENT = str(sys.argv[0]).lower()

    if not upload_to_s3('/tmp/artifact.zip'):
        sys.exit(1)
    if not deploy_new_revision():
        sys.exit(1)

if __name__ == "__main__":
    main()