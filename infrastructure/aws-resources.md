# AWS PrivateLink Third-Party API - Infrastructure

## AWS Region

- Region: Asia Pacific (Mumbai)
- Region Code: ap-south-1

## Architecture

Consumer EC2
    |
    v
Interface VPC Endpoint
    |
    v
AWS PrivateLink
    |
    v
Endpoint Service
    |
    v
Internal Network Load Balancer
    |
    v
Nginx Reverse Proxy
    |
    v
FastAPI Application

## Provider VPC

- VPC Name: provider-vpc
- CIDR: 10.0.0.0/16

### Provider Subnets

- provider-public-a: 10.0.1.0/24
- provider-public-b: 10.0.2.0/24

### Provider EC2

- Name: provider-server
- Operating System: Ubuntu 26.04 LTS
- Instance Type: t3.micro
- Private IP: 10.0.1.132
- Application Port: 8000
- Nginx Port: 80

### Network Load Balancer

- Name: provider-nlb
- Type: Network Load Balancer
- Scheme: Internal
- Listener: TCP 80
- Target Group: provider-tg
- Target Port: 80
- Health Check: HTTP /

## VPC Endpoint Service

- Name: provider-endpoint-service
- Backend Load Balancer: provider-nlb
- Acceptance Required: Enabled
- Service Type: AWS PrivateLink

## Consumer VPC

- VPC Name: consumer-vpc
- CIDR: 10.1.0.0/16

### Consumer Subnet

- Name: consumer-subnet-a
- CIDR: 10.1.1.0/24

### Consumer EC2

- Name: consumer-server
- Operating System: Ubuntu 26.04 LTS
- Instance Type: t3.micro
- Private IP: 10.1.1.26
- Public IP: None

## Interface VPC Endpoint

- Name: consumer-privatelink-endpoint
- Type: Interface
- Service: provider-endpoint-service
- VPC: consumer-vpc
- IP Address Type: IPv4
- Status: Available

## EC2 Instance Connect Endpoint

- Name: Consumer EC2 Instance Connect Endpoint
- Used to securely connect to the private consumer EC2 instance without assigning a public IP.

## Application

The provider hosts a REST API built with Python FastAPI.

### API Endpoints

- GET /
- GET /api/students
- GET /api/students/{id}
- POST /api/students
- DELETE /api/students/{id}

FastAPI documentation is available at:

/docs

## PrivateLink Traffic Flow

1. Consumer EC2 sends an API request.
2. Request reaches the Interface VPC Endpoint.
3. AWS PrivateLink securely connects the consumer VPC to the provider Endpoint Service.
4. Endpoint Service forwards traffic to the internal Network Load Balancer.
5. NLB forwards traffic to the provider EC2 instance.
6. Nginx receives traffic on port 80.
7. Nginx reverse-proxies the request to FastAPI on port 8000.
8. FastAPI processes the request and returns the response.

## Security

The provider application is not directly exposed to the public internet through the PrivateLink service.

The consumer EC2 instance does not require a public IP address.

Security groups are used to control traffic between the consumer resources and the PrivateLink endpoint.

## Testing

The API was successfully tested from the consumer EC2 instance through the PrivateLink endpoint.

Example:

curl http://<PRIVATE_ENDPOINT_DNS>/api/students

The request returned student data from the provider FastAPI application.

Direct access to the provider EC2 private IP was also tested and was not reachable from the consumer VPC.

This demonstrates private service-to-service connectivity using AWS PrivateLink.
