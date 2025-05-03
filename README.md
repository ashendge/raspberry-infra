# raspberry-infra
Raspberry infrastructure related and networking projects

# Raspberry Pi Infrastructure Lab

A hands-on homelab built on a Raspberry Pi 4, combining real-world networking, monitoring, and Infrastructure as Code (IaC) projects to sharpen system design and DevOps skills.

---

## Table of Contents
- [Project 1: DNS Server (Pi-hole + Unbound)](#project-1-dns-server-pi-hole--unbound)
- [Project 2: Network Monitoring (Grafana + Prometheus)](#project-2-network-monitoring-grafana--prometheus)
- [Project 3: Infrastructure as Code (Terraform + Docker)](#project-3-infrastructure-as-code-terraform--docker)
- [Hardware Used](#hardware-used)
- [Future Enhancements](#future-enhancements)

---

## Project 1: DNS Server (Pi-hole + Unbound)

### Overview
A self-hosted DNS server that blocks ads and trackers while resolving domains via a local recursive resolver (Unbound).

### Stack
- [Pi-hole](https://pi-hole.net/)
- [Unbound](https://nlnetlabs.nl/projects/unbound/about/)

### Setup Steps
1. Install Pi-hole on Raspberry Pi
2. Configure your device’s DNS to point to Pi-hole (e.g., `192.168.1.100`)
3. Install Unbound for recursive DNS
4. Configure Pi-hole to forward DNS to Unbound (`127.0.0.1#5335`)
5. Verify using `dig` and `nslookup`

### Screenshot / Demo
_Add Grafana graphs or `dig` output here later._

---

## Project 2: Network Monitoring (Grafana + Prometheus)

### Overview
A dashboard for monitoring home network traffic, latency, system health, and uptime across devices.

### Stack
- [Grafana](https://grafana.com/)
- [Prometheus](https://prometheus.io/)
- [Node Exporter / Pi.Alert](https://github.com/pucherot/Pi.Alert) for system and network metrics

### Setup Steps
1. Install Prometheus and Grafana (via Docker or native)
2. Add Prometheus data source to Grafana
3. Use Node Exporter or Pi.Alert to expose metrics
4. Create dashboards to monitor:
   - Raspberry Pi CPU/RAM
   - Connected devices
   - Ping latency
   - Speedtest (optional)

### Screenshot / Demo
_Add sample dashboards or Pi.Alert UI screenshots._

---

## Project 3: Infrastructure as Code (Terraform + Docker)

### Overview
Automate infrastructure on the Raspberry Pi using Terraform to define and deploy containers like Grafana, Prometheus, and Pi-hole.

### Stack
- [Terraform](https://www.terraform.io/)
- [Docker](https://www.docker.com/)
- Raspberry Pi OS (64-bit recommended)

### Goals
- Use Terraform to define infrastructure in `.tf` files
- Provision Docker containers for monitoring and DNS
- Simulate real-world IaC workflows

### Basic Terraform Project Structure



