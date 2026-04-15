# Use a lightweight python image
FROM python:3.10-slim

# Create a working directory inside the container
WORKDIR /app

# Add a non-root user to adhere to Hugging Face Spaces security protocols
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy the requirements file into the container
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY --chown=user . .

# Hugging Face Spaces exposes port 7860 to the web
EXPOSE 7860

# Command to run the Flask application securely
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]
