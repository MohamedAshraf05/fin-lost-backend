# 1️⃣ Start from an official Python image
FROM python:3.11-slim

# 2️⃣ Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# 3️⃣ Set the working directory
WORKDIR /app

# 4️⃣ Install system dependencies and clean cache
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    netcat-traditional \
    default-libmysqlclient-dev \
    default-mysql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copy requirements first (to leverage Docker caching)
COPY requirements.txt .

# 6️⃣ Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7️⃣ Copy project files
COPY . .

# 8️⃣ Ensure wait_for_db.sh is executable
RUN chmod +x /app/wait_for_db.sh

# 9️⃣ Expose port
EXPOSE 8000

# 🔟 Use the dynamic startup script (it decides: dev vs prod)
CMD ["sh", "/app/wait_for_db.sh"]
