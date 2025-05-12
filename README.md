# README: Inštalácia Ruby, Ruby on Rails a Python na Linux

Tento dokument poskytuje podrobné inštrukcie na inštaláciu **Ruby**, **Ruby on Rails** a **Pythonu** na systémoch Linux (Debian, Ubuntu, Arch, Fedora a Alpine Linux).

---

## 1. Inštalácia Ruby

### **Debian/Ubuntu**
```sh
sudo apt update && sudo apt install -y ruby-full build-essential
```

Overenie inštalácie:
```sh
ruby -v
```

### **Fedora**
```sh
sudo dnf install -y ruby
```

### **Arch Linux**
```sh
sudo pacman -S ruby
```

### **Alpine Linux**
```sh
apk add ruby
```

---

## 2. Inštalácia Ruby on Rails

Rails je framework pre Ruby, ktorý je potrebné inštalovať cez **gem**.

```sh
gem install rails -N
```

Overenie inštalácie:
```sh
rails -v
```

Ak sa vyskytne chyba, skontrolujte, či je Ruby správne nainštalovaný a či je `gem` dostupný.

---

## 3. Inštalácia Pythonu

### **Debian/Ubuntu**
```sh
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```

Overenie inštalácie:
```sh
python3 --version
pip3 --version
```

### **Fedora**
```sh
sudo dnf install -y python3 python3-pip
```

### **Arch Linux**
```sh
sudo pacman -S python python-pip
```

### **Alpine Linux**
```sh
apk add python3 py3-pip
```

---

## 4. Nastavenie Virtuálneho Prostredia v Pythone

Odporúča sa používať virtuálne prostredie na izoláciu Python projektov:

```sh
python3 -m venv venv
source venv/bin/activate
```

Deaktivácia virtuálneho prostredia:
```sh
deactivate
```

---

## 5. Instalacia ruby gems a python requirements

v root projektu spustit tento command

```sh
bundle install
```

Nasledovne prejst do python_api directory a spustit tento command

```sh
pip install requirements
```

## 6. Spustenie projektu

V root projektu spustit server

```sh
bin/dev
```
Navigovat na dany localhost a je to hotove.

## Docker Deployment

This project can be deployed using Docker for production environments. Here's how:

### 1. Build the Docker Image
```bash
docker build -t matura .
```

### 2. Generate Rails Master Key (if you haven't)
```bash
# Run this in your project directory before building:
EDITOR="nano" rails credentials:edit
```

### 3. Run the Container
```bash
docker run -d \
  -p 80:80 \
  -p 8000:8000 \
  -e RAILS_MASTER_KEY=$(cat config/master.key) \
  -e DATABASE_URL=your_postgres_connection_string \
  --name matura \
  matura
```

### 4. Required Environment Variables
- `RAILS_MASTER_KEY`: Contents of your `config/master.key` file
- `DATABASE_URL`: Postgres connection string (e.g. `postgres://user:password@host:port/db_name`)

### 5. Additional Configuration
For production, you may also want to set:
```bash
-e RAILS_ENV=production \
-e SECRET_KEY_BASE=your_generated_secret \
```

### 6. Using Docker Compose
Create a `docker-compose.yml` file:
```yaml
version: '3'
services:
  app:
    image: matura
    ports:
      - "80:80"
      - "8000:8000"
    environment:
      - RAILS_MASTER_KEY=${RAILS_MASTER_KEY}
      - DATABASE_URL=postgres://postgres:password@db:5432/matura_production
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=matura_production
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Then run:
```bash
echo "RAILS_MASTER_KEY=$(cat config/master.key)" > .env
docker compose up -d
```

### 7. Viewing Logs
```bash
docker logs -f matura
```

### 8. Stopping the Container
```bash
docker stop matura
docker rm matura
```

Note: For production deployments, consider using:
- [Kamal](https://kamal-deploy.org) (included in this project)
- Kubernetes
- AWS ECS/Fargate
