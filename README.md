# Clipsify
[![CodeQL](https://github.com/timkrebs9/Clipsipfy/actions/workflows/codeql.yml/badge.svg)](https://github.com/timkrebs9/Clipsipfy/actions/workflows/codeql.yml)
[![pre-commit](https://github.com/timkrebs9/Clipsipfy/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/timkrebs9/Clipsipfy/actions/workflows/pre-commit.yml)
[![aks-converter](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-converter.yaml/badge.svg?branch=main)](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-converter.yaml)
[![aks-gateway](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-gateway.yaml/badge.svg?branch=main)](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-gateway.yaml)
[![aks-notification](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-notification.yaml/badge.svg?branch=main)](https://github.com/timkrebs9/Clipsipfy/actions/workflows/aks-notification.yaml)


## Overview

Clipsify is an innovative web application designed to convert MP4 video files into MP3 format, allowing users to extract audio from videos quickly and easily. This project utilizes a robust backend built on Python with integration of MongoDB, Kubernetes, RabbitMQ, and Azure services, ensuring scalable and efficient performance.

## Features

- **Video to Audio Conversion**: Convert any MP4 video file into an MP3 audio file.
- **User-Friendly Interface**: Simple and intuitive web interface for easy operation.
- **High Efficiency**: Leverages RabbitMQ for message queuing to handle high loads and asynchronous processing.

## Folder Structure

Below is an outline of the key directories and files within the Clipsify repository:

```plaintext
/Clipsify
│
├── app                     # Application source files
│   ├── gateway             # Gateway service for handling requests
│   │   ├── server.py       # Main server file
│   │   ├── config.py       # Configuration settings
│   ├── auth                # Authentication services
│   │   ├── auth.py         # Authentication logic
│   ├── utils               # Utility scripts and helper functions
│   │   ├── logger.py       # Logging utility
│
├── k8s                     # Kubernetes deployment configurations
│   ├── deployment.yaml     # Deployment configuration
│   ├── service.yaml        # Service definition
│
├── helm                    # Helm charts for Kubernetes deployment
│   ├── charts              # Charts for various services
│
├── docs                    # Documentation files
│   ├── api.md              # API documentation
│
├── test                    # Test scripts and test cases
│   ├── test_server.py      # Unit tests for server components
│
└── README.md
```

## Installation

To set up Clipsify on your local machine or deployment environment, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/timkrebs9/Clipsify.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Clipsify
   ```

3. **Install dependencies** (ensure you have Python and Docker installed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the services** (using Docker and Kubernetes):
   ```bash
   docker-compose up --build
   kubectl apply -f k8s/
   ```

## Usage

After installation, you can access the Clipsify web interface at `http://localhost:8080` by default. Use the interface to upload MP4 files and convert them to MP3 format.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

See `LICENSE` for more information.


### Connect to an AKS Cluster With Azure CLI and Kubectl


To connect to an  Azure AKS cluster, first, we need to login to  Azure using the following command:

```powershell
az login
```
If you have more than one subscription, set it using the following command:

```powershell	
az account set --subscription subname 
```
After login to Azure, install the Kubectl command line tools plug-in for Azure CLI using the following line:

```powershell	
az aks install-cli
```
Finally, we run the following command to authenticate to our AKS cluster. Make sure you fill in the resource group name of your cluster and your cluster name:

```powershell
az aks get-credentials --resource-group RGNAME --name CLUSTERNAME
```

You can type kubectl, access the help file, and start managing your AKS cluster.
