# AWS PrivateLink Third-Party API

A real REST API built with **Python FastAPI** and securely exposed between two isolated AWS VPCs using **AWS PrivateLink**.

## Project Overview

This project demonstrates how a consumer application can securely access a third-party API without requiring direct network connectivity or exposing the provider application to the public internet.

The architecture uses:

**Consumer EC2 → Interface VPC Endpoint → AWS PrivateLink → Endpoint Service → Internal NLB → Nginx → FastAPI**

## Architecture

```text
┌──────────────────────┐
│     Consumer VPC     │
│                      │
│  ┌────────────────┐  │
│  │  Consumer EC2  │  │
│  └───────┬────────┘  │
│          │           │
│          ▼           │
│  ┌────────────────┐  │
│  │ Interface VPC  │  │
│  │    Endpoint     │  │
│  └───────┬────────┘  │
└──────────┼───────────┘
           │
           │ AWS PrivateLink
           │
┌──────────▼───────────┐
│    Provider VPC      │
│                      │
│  ┌────────────────┐  │
│  │ Endpoint       │  │
│  │ Service        │  │
│  └───────┬────────┘  │
│          │           │
│          ▼           │
│  ┌────────────────┐  │
│  │ Internal NLB   │  │
│  └───────┬────────┘  │
│          │           │
│          ▼           │
│  ┌────────────────┐  │
│  │     Nginx      │  │
│  │      :80       │  │
│  └───────┬────────┘  │
│          │           │
│          ▼           │
│  ┌────────────────┐  │
│  │ FastAPI :8000  │  │
│  └────────────────┘  │
└──────────────────────┘
```

## AWS Services Used

* Amazon VPC
* Amazon EC2
* AWS PrivateLink
* Interface VPC Endpoint
* VPC Endpoint Service
* Network Load Balancer
* Security Groups
* EC2 Instance Connect Endpoint
* Nginx
* Python FastAPI

## AWS Region

**Asia Pacific (Mumbai)**

Region:

```text
ap-south-1
```

## Provider VPC

```text
VPC: provider-vpc
CIDR: 10.0.0.0/16
```

Provider subnets:

```text
provider-public-a: 10.0.1.0/24
provider-public-b: 10.0.2.0/24
```

Provider EC2:

```text
Name: provider-server
Instance Type: t3.micro
Private IP: 10.0.1.132
```

## Consumer VPC

```text
VPC: consumer-vpc
CIDR: 10.1.0.0/16
```

Consumer subnet:

```text
consumer-subnet-a
CIDR: 10.1.1.0/24
```

Consumer EC2:

```text
Name: consumer-server
Instance Type: t3.micro
Private IP: 10.1.1.26
Public IP: None
```

## REST API

The provider application is built using **FastAPI**.

### Available Endpoints

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| GET    | `/`                  | API health/status      |
| GET    | `/api/students`      | Get all students       |
| GET    | `/api/students/{id}` | Get a specific student |
| POST   | `/api/students`      | Create a student       |
| DELETE | `/api/students/{id}` | Delete a student       |

Interactive API documentation:

```text
/docs
```

FastAPI automatically provides Swagger UI at:

```text
http://<PRIVATE_ENDPOINT_DNS>/docs
```

## Example API Response

Request:

```text
GET /api/students
```

Response:

```json
[
  {
    "id": 1,
    "name": "Ponish",
    "course": "B.Tech",
    "attendance": 87
  },
  {
    "id": 2,
    "name": "Rahul",
    "course": "B.Tech",
    "attendance": 91
  }
]
```

## PrivateLink Traffic Flow

1. The consumer EC2 sends an HTTP request.
2. The request reaches the Interface VPC Endpoint.
3. AWS PrivateLink establishes private connectivity to the provider Endpoint Service.
4. The Endpoint Service forwards traffic to the internal Network Load Balancer.
5. The NLB forwards traffic to the healthy provider EC2 target.
6. Nginx receives the request on port 80.
7. Nginx reverse-proxies the request to FastAPI on port 8000.
8. FastAPI processes the request.
9. The response travels back through the same private connectivity path.

## Nginx Configuration

Nginx acts as a reverse proxy.

```text
Port 80 → Nginx → Port 8000 → FastAPI
```

This allows the existing NLB and PrivateLink configuration to continue using TCP port 80 while the FastAPI application runs on port 8000.

## Testing

The API was successfully tested from the private consumer EC2 instance.

Example:

```bash
curl http://<PRIVATE_ENDPOINT_DNS>/
```

Expected response:

```json
{
  "message": "AWS PrivateLink API is running",
  "service": "Third-Party Student API",
  "status": "success"
}
```

Student API test:

```bash
curl http://<PRIVATE_ENDPOINT_DNS>/api/students
```

The request successfully returned student data from the provider FastAPI application.

## Security Demonstration

The consumer EC2 instance does not have a public IP address.

The provider application is accessed through AWS PrivateLink rather than direct public access.

Direct access to the provider EC2 private IP from the consumer VPC was also tested and was not reachable.

This demonstrates private service-to-service connectivity using AWS PrivateLink.

## Project Structure

```text
aws-privatelink-third-party-api/
│
├── api/
│   ├── app.py
│   └── requirements.txt
│
├── infrastructure/
│   └── aws-resources.md
│
├── screenshots/
│
├── README.md
│
├── .gitignore
│
└── LICENSE
```

## Running the API

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI application:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available on:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Key Learning Outcomes

This project demonstrates:

* AWS VPC networking
* Network Load Balancer configuration
* AWS PrivateLink
* VPC Endpoint Services
* Interface VPC Endpoints
* Private EC2 networking
* Security Group configuration
* Nginx reverse proxy
* REST API development using FastAPI
* End-to-end private API connectivity
* Testing private service access

## Conclusion

This project demonstrates how AWS PrivateLink can be used to securely expose a third-party REST API to consumers without requiring public internet access or direct VPC-to-VPC networking.

The final implementation provides a realistic private API architecture using AWS networking and modern REST API technologies.
