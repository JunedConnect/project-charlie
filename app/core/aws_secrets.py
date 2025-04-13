import boto3
import json
from botocore.exceptions import ClientError


def get_aws_secret(secret_name: str, region_name: str = 'eu-west-2') -> dict:
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response["SecretString"]
        return json.loads(secret)
    except ClientError as e:
        raise Exception(f"Could not retrieve secret {secret_name}: {e}")
