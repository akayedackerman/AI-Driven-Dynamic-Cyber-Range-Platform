# dockerfiles/nginx-iptables.Dockerfile
# Use the official Nginx image as a base
FROM nginx:latest

# Install iptables
# Use apt-get update and install in a single RUN command to reduce image layers
# and clean up apt cache to keep image size down.
RUN apt-get update && \
    apt-get install -y iptables && \
    rm -rf /var/lib/apt/lists/*

# Keep the original Nginx entrypoint and command
# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["nginx", "-g", "daemon off;"]