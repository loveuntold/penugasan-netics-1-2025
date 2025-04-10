# Laporan Penugasan 1 NETICS

**Link DockerHub**

https://hub.docker.com/repository/docker/loveuntold/ci-cd-api

**Link URL API**

http://44.202.58.239:8000/health

<br>
<br>
<br>

> **Buatlah API publik dengan endpoint /health.**
  
   Di sini saya menggunakan framework FastAPI di Python.
   
   ```c
   from fastapi import FastAPI
   from datetime import datetime
   from time import time
   ```
  Pertama, import library.


  ```c
  app = FastAPI()
  ```
  Lalu, insiasi untuk mendefiniskan endpoint.

  ```c
  @app.get("/health")
  async def health():
      return {
          "nama": "Ayesha Nayla Satrio",
          "nrp": "5025231195",
          "status": "UP",
          "timestamp": datetime.now(),
          "uptime": time()
      }
  ```
<br>
<br>
<br>

> **Lakukan deployment API tersebut dalam bentuk container (Docker Multi-stage) pada VPS publik.
> Endpoint `/health` dapat diakses menggunakan GET. Nantinya informasi akan direturn.**

  ```c
  FROM python:3.11-slim AS builder
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt
  COPY . .
  
  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages
  COPY --from=builder /app .
  CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

  Pertama, buat `Dockerfile`. Pada tahap pertama, image python diinstall. Lalu, `requirements.txt` disalin kedalam container dan menginstall ke dalam `/app/deps`. Setelah itu, seluruh code app disalin ke dalam container. 
  Pada tahap kedua, hanya menyalin code app dari tahap pertama, tanpa membawa file build yang tidak diperlukan. Aplikasi dijalankan menggunakan Uvicorn pada host `0.0.0.0` dan port `8000`.

<br>
<br>
<br>

> **Lakukan proses CI/CD menggunakan GitHub Actions untuk melakukan otomasi proses deployment API.**

  CI/CD pada Github Actions akan secara otomatis membangun dan melakukan deploy aplikasi FastAPI setiap kali ada push atau pull request ke branch main. 

  ```c
  jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Log in to Docker Hub
        run: echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin

      - name: Build Docker image
        run: docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/ci-cd-api:latest .

      - name: Push Docker image
        run: docker push ${{ secrets.DOCKERHUB_USERNAME }}/ci-cd-api:latest
  ```
  Job ini berjalan di ubuntu-latest dan terdiri dari langkah-langkah berikut:
  1. Checkout code: Mengambil source code dari repository.
  2. Login ke docker hub 
  3. Build Docker image: Membangun image Docker dari Dockerfile.
  4. Push Docker image
     
  ```c
    deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: SSH to server and deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            echo "Pulling latest image..."
            docker stop ci-cd-api || true
            docker rm ci-cd-api || true
            docker pull ${{ secrets.DOCKERHUB_USERNAME }}/ci-cd-api:latest
            docker run -d -p 8000:8000 --name ci-cd-api ${{ secrets.DOCKERHUB_USERNAME }}/ci-cd-api:latest
            echo "Deployment complete."
  ```
  Job ini dijalankan setelah tahap build selesai. 
  1. SSH ke server VPS menggunakan credentials yang tersimpan di GitHub Secrets.
  2. Pull image dari Docker Hub (loveuntold/ci-cd-api:latest).
  3. Jika ada container lama, maka akan dihentikan dan dihapus.
  4. Menjalankan container baru dengan port 8000.

  Berikut adalah Github Secret yang ditambahkan:
  - VPS_HOST: Public IP VPS.
  - VPS_USER: Username login VPS (ec2-user).
  - VPS_SSH_KEY: Private key SSH.
  - DOCKERHUB_USERNAME: Username Docker Hub
  - DOCKERHUB_TOKEN: Password Docker Hub

<br>
<br>
<br>

> **Hasil**

![image](https://github.com/user-attachments/assets/52414c28-7311-42b4-9e99-d5adcb826dbd)


  
  


  

  
  
