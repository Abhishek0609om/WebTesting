# Enterprise User Portal (`ocptest.store`)

A secure, production-ready enterprise web application architecture built with a **FastAPI** backend, **MongoDB** database, and **Nginx** reverse proxy with **TLS/SSL termination**, hosted on **AWS** using a multi-tier VPC network design.

---

## **Architecture Overview**

The project separates public-facing services from internal database storage across public and private subnets, ensuring high security and data isolation.

```text
 ┌────────────────────────────────────────────────────────┐
 │                      END USER                          │
 │         (Browser visiting https://ocptest.store)       │
 └───────────────────────────┬────────────────────────────┘
                             │ HTTPS (Port 443) [Let's Encrypt SSL]
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │ PUBLIC EC2 INSTANCE (IP: 43.204.200.223 / 10.0.7.106)  │
 │                                                        │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ NGINX (Reverse Proxy & TLS Termination)          │  │
 │  └────────────────────────┬─────────────────────────┘  │
 │                           │ HTTP (Port 8000 - Local)   │
 │                           ▼                            │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ FastAPI Backend (Docker Container)               │  │
 │  └────────────────────────┬─────────────────────────┘  │
 └───────────────────────────┼────────────────────────────┘
                             │ Private Subnet Connection
                             │ [MongoDB Wire Protocol: Port 27017]
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │ PRIVATE EC2 INSTANCE (IP: 10.0.128.190)                │
 │                                                        │
 │  ┌──────────────────────────────────────────────────┐  │
 │  │ MongoDB Database (crud_database)                 │  │
 │  │  • Authenticated via abhi / abhi@1234            │  │
 │  └──────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────┘
```

---

<img width="1024" height="782" alt="WhatsApp Image 2026-11-12 at 9 41 34 PM" src="https://github.com/user-attachments/assets/50d14075-0d6a-4505-a45b-7a9946eb60dd" />


## **Tech Stack**

* **Frontend / UI:** HTML5 / CSS3 Portal Dashboard
* **Backend Framework:** FastAPI (Python, asynchronous API)
* **Web Server & Proxy:** Nginx (Reverse proxy, HTTP/HTTPS handling)
* **SSL / TLS Automation:** Certbot & Let's Encrypt
* **Database:** MongoDB (Document-oriented NoSQL database)
* **Cloud & Infrastructure:** Amazon Web Services (AWS VPC, Public/Private Subnets, Internet Gateway, NAT Gateway, Elastic IP, Security Groups)

---

## **Infrastructure Components**

| Component | Type / Role | Description |
| :--- | :--- | :--- |
| **`ocptest.store`** | Domain Name | Points via DNS A-Record to the public Elastic IP (`43.204.200.223`). |
| **Public EC2 Instance** | App & Proxy Server (`10.0.7.106`) | Hosts Nginx (TLS termination) and the FastAPI Docker container. |
| **Private EC2 Instance** | Database Server (`10.0.128.190`) | Isolated in a private subnet running MongoDB (`crud_database`). |
| **NAT Gateway** | Outbound Network Gateway | Enables secure outbound internet access for private subnet instances. |
| **Internet Gateway (IGW)** | VPC Edge Gateway | Manages inbound traffic from the internet to the public subnet. |

---

## **Security & Authentication**

* **TLS Termination:** All incoming public browser traffic is encrypted via HTTPS (Port 443) using a trusted Let's Encrypt SSL certificate managed by Nginx.
* **Database Security:** MongoDB requires authentication (`abhi` / `abhi@1234`) targeting `crud_database` and is protected by security group rules that strictly restrict access to internal application subnets on port `27017`.
* **Network Isolation:** Private database instances are shielded from direct public internet exposure.

---

## **Getting Started & Deployment**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/WebTesting.git
cd WebTesting
```

### **2. Run FastAPI Backend (Docker)**
Build and start the containerized backend service:
```bash
docker build -t fastapi-backend .
docker run -d -p 8000:8000 --name portal-backend fastapi-backend
```

### **3. Configure Nginx & SSL (Certbot)**
Install Nginx and configure the server block for `ocptest.store`:
```bash
sudo dnf install nginx certbot python3-certbot-nginx -y
sudo systemctl start nginx
```
Run Certbot to fetch the SSL certificate and enable HTTPS:
```bash
sudo certbot --nginx -d ocptest.store -d www.ocptest.store
```
