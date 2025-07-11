# Use official Red Hat UBI Python image for better OpenShift compatibility
FROM registry.access.redhat.com/ubi9/python-3.11

# Set working directory
WORKDIR /app

# Copy requirements (if any)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Ensure permissions for OpenShift random UID
RUN chgrp -R 0 /app && chmod -R g=u /app

# Set unprivileged user
USER 1001

# Expose port (optional, depending on your app)
EXPOSE 8080

# Set default command
CMD ["python", "kafka.py"]

