# iac/main.tf

# Required Docker provider
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

# Docker provider configuration
provider "docker" {}

# --- Define Network for the Scenario ---
resource "docker_network" "scenario_net" {
  name = "cyber_range_scenario_network"
  # Using bridge driver which is default and suitable for isolated local networks
  driver = "bridge"
}

# --- Define Docker Images ---
# Nginx Web Server Image
resource "docker_image" "nginx_image" {
  name = "nginx:latest"
  keep_locally = true # Keep the image after terraform destroy
}

# Ubuntu Image (as a base for an "app server" placeholder)
resource "docker_image" "ubuntu_app_image" {
  name = "ubuntu:latest"
  keep_locally = true
}

# MySQL Database Image
resource "docker_image" "mysql_image" {
  name = "mysql:5.7" # Using a specific stable version for consistency
  keep_locally = true
}

# --- Define Docker Containers (Scenario Environment) ---

# 1. Web Server Container (e.g., frontend)
resource "docker_container" "web_server" {
  name  = "scenario_web_server"
  image = docker_image.nginx_image.name
  ports {
    internal = 80
    external = 8080 # Expose to host for easy access
  }
  networks_advanced {
    name = docker_network.scenario_net.name
    aliases = ["web"] # Alias for easy resolution within the network
  }
  # Ensure network is created before container
  depends_on = [docker_network.scenario_net]
}

# 2. Application Server Container (placeholder for business logic)
resource "docker_container" "app_server" {
  name  = "scenario_app_server"
  image = docker_image.ubuntu_app_image.name
  # This command just keeps the container running and installs Python for the simple http server
  command = ["/bin/bash", "-c", "apt update && apt install -y python3 && python3 -m http.server 8000 & wait $!"]
  networks_advanced {
    name = docker_network.scenario_net.name
    aliases = ["app"]
  }
  depends_on = [docker_network.scenario_net]
}

# 3. Database Server Container
resource "docker_container" "db_server" {
  name  = "scenario_db_server"
  image = docker_image.mysql_image.name
  # WARNING: Hardcoded password - For demonstration only!
  env = [
    "MYSQL_ROOT_PASSWORD=veryinsecurepassword",
    "MYSQL_DATABASE=my_app_db",
    "MYSQL_USER=app_user",
    "MYSQL_PASSWORD=app_password"
  ]
  networks_advanced {
    name = docker_network.scenario_net.name
    aliases = ["db"]
  }
  depends_on = [docker_network.scenario_net]
}