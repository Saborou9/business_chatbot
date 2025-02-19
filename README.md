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
