# Envoy AI Gateway with Amazon Bedrock Integration

## Introduction
This repository contains sample notebook to demonstrates the use of Envoy AI Gateway ([https://aigateway.envoyproxy.io/docs](https://aigateway.envoyproxy.io/docs)) along with various backend AI services including Amazon Bedrock and other 3P model providers. The Envoy AI Gateway facilitates the management of AI service traffic, enabling features like routing, authentication, and security policies for AI applications.


## Pre-requisites
Ensure the following tools are installed before proceeding:

1.  **kubectl**: The Kubernetes command-line tool.
2.  **helm**: The package manager for Kubernetes.
3.  **curl**: For testing API endpoints (installed by default on most systems).
4.  **AWS CLI**: AWS command line interface.

Note that we will leverage Amazon EKS service as the hosting platform for Envoy AI Gateway. 
Follow along the step by step guide in the `01-ai-gatewat-with-bedrock.ipynb` notebook to get started.


