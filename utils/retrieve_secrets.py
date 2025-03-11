import boto3
import yaml
import os

def get_secret(secret_name, region_name):
    """
    Retrieves a secret from AWS Secrets Manager.

    Args:
        secret_name (str): The name of the secret.
        region_name (str): The AWS region the secret is stored in.

    Returns:
        dict: A dictionary containing the secret data, or None if an error occurs.
    """
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None

    import json  # Import json here, inside the function
    secret = json.loads(get_secret_value_response['SecretString'])
    return secret

def update_yaml(yaml_file, aws_access_key_id, aws_secret_access_key, openai_api_key):
    """
    Updates the YAML file with the AWS credentials and OpenAI API key.

    Args:
        yaml_file (str): Path to the YAML file.
        aws_access_key_id (str): The AWS Access Key ID.
        aws_secret_access_key (str): The AWS Secret Access Key.
        openai_api_key (str): The OpenAI API key.
    """
    with open(yaml_file, 'r') as f:
        yaml_data = yaml.safe_load_all(f)  # Use safe_load_all to handle multiple documents

        updated_yaml_data = []  # Store updated documents

        for doc in yaml_data:
            if doc:
                if doc.get('kind') == 'Secret' and doc['metadata']['name'] == 'envoy-ai-gateway-basic-aws-credentials':
                    # Update the AWS credentials secret
                    doc['stringData']['credentials'] = f"[default]\naws_access_key_id = {aws_access_key_id}\naws_secret_access_key = {aws_secret_access_key}"
                elif doc.get('kind') == 'Secret' and doc['metadata']['name'] == 'envoy-ai-gateway-basic-openai-apikey':
                    # Update the OpenAI API key secret
                    doc['stringData']['apiKey'] = openai_api_key
                updated_yaml_data.append(doc)

    # Write the updated YAML data back to the file
    with open(yaml_file, 'w') as f:
        yaml.dump_all(updated_yaml_data, f, default_flow_style=False)

def main():
    """
    Main function to retrieve secrets and update the YAML file.
    """
    # AWS Configuration - Modify these as needed
    region_name = "<YOUR_AWS_REGION>"  # Replace with your AWS region
    aws_secret_name = "<YOUR_AWS_SECRET_NAME>"  # Replace with your AWS secret name in Secrets Manager
    openai_secret_name = "<YOUR_OPEN_AI_SECRET_NAME>" # Replace with your OpenAI secret name
    yaml_file = "./basic.yaml" # Replace with the name of your YAML file

    # Retrieve secrets from AWS Secrets Manager
    aws_secrets = get_secret(aws_secret_name, region_name)
    openai_secrets = get_secret(openai_secret_name, region_name)

    if aws_secrets and openai_secrets:
        aws_access_key_id = aws_secrets.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = aws_secrets.get('AWS_SECRET_ACCESS_KEY')
        openai_api_key = openai_secrets.get('OPENAI_API_KEY')

        if aws_access_key_id and aws_secret_access_key and openai_api_key:
            # Update the YAML file
            update_yaml(yaml_file, aws_access_key_id, aws_secret_access_key, openai_api_key)
            print("YAML file updated successfully!")
        else:
            print("One or more secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, OPENAI_API_KEY) not found in Secrets Manager.")
    else:
        print("Failed to retrieve secrets from AWS Secrets Manager.")

if __name__ == "__main__":
    main()
