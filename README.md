# 📡 Real-Time Environmental Sensor Data Pipeline

This project implements a real-time data pipeline using **Apache Kafka**, **Docker**, and **PostgreSQL** to simulate and process environmental sensor data from a CSV file. The pipeline mimics live IoT sensor streaming and stores the data for further analysis.

---

## 🚀 Project Overview

- 📁 Source: Kaggle Dataset – *Environmental Sensor Data (132k rows)*
- 🔄 Simulates real-time sensor data with `pandas`
- 🔌 Streams data into **Kafka topics** using a Python producer
- 📥 Kafka consumer reads the stream and stores it in **PostgreSQL**
- 🐳 Fully containerized with **Docker Compose**
- 📊 Kafka-UI for topic monitoring

---

## 🛠️ Technologies Used

| Component        | Tech Stack                     |
|------------------|--------------------------------|
| Data Streaming   | Apache Kafka                   |
| Messaging System | Kafka-Python (`kafka-python`)  |
| Data Ingestion   | Python + Pandas                |
| Database         | PostgreSQL                     |
| Orchestration    | Docker + Docker Compose        |
| Monitoring       | Kafka-UI (ProvectusLabs)       |

---

## 🗂️ Project Structure
```bash
elective2/
├── dataset/
│ └── iot_telemetry_data.csv
├── producer/
│ ├── producer.py
│ ├── requirements.txt
│ └── Dockerfile
├── consumer/
│ ├── consumer.py
│ ├── requirements.txt
│ └── Dockerfile
├── logs/
│ ├── consumer.log
│ ├── producer.log
├── db/
│ └── init.sql
├── docker-compose.yml
└── README.md
```
---

## 🧠 Kafka Topic

- **Topic Name**: `kafka-topic-postgress`
- **Created Dynamically** if not already present
- Partitions: `1`
- Replication: `1`

---

## 🧪 How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/gulomovazukhrakhon/elective2.git
cd elective2
```
### 2. Run Docker Compose
```bash
docker-compose up --build
``` 

This will start:
* Kafka + Zookeeper
* PostgreSQL
* Producer and Consumer
* Kafka-UI on port `8080`

### 3. Access Kafka UI
📍 Open: http://localhost:8080
<br>
🧠 Topic: kafka-topic-postgress

---

## 🗄️ PostgreSQL Table: telemtry_data
Created automatically via init.sql. Structure:

| Column   | Type             |
|----------|------------------|
| ts       | DOUBLE PRECISION |
| device   | TEXT             |
| co       | DOUBLE PRECISION |
| humidity | DOUBLE PRECISION |
| light    | BOOLEAN          |
| lpg      | DOUBLE PRECISION |
| motion   | BOOLEAN          |
| smoke    | DOUBLE PRECISION |
| temp     | DOUBLE PRECISION |

---

## 🧾 Logging and Monitoring

Both Python services implement robust logging using the `logging` module:
- Logs include timestamps, levels (INFO, WARNING, ERROR)
- Logged to both Docker container stdout and `.log` files inside the `/logs` directory
- Helpful for debugging retries, Kafka/DB issues, and success confirmations

Logs are visible via:
```bash
docker logs kafka-producer
docker logs kafka-consumer
```
---

## 🔍 How It Works

1. producer.py reads CSV row by row
2. Sends each row as a JSON message to Kafka
3. Kafka holds messages under kafka-topic-postgress
4. consumer.py listens to the topic and inserts each message into PostgreSQL
5. Kafka UI displays messages in real-time

---

## ✅ Project Highlights

* ⏱️ Simulated real-time streaming (5s delay)
* 💾 Durable storage with PostgreSQL
* 🛡️ Error handling and retry logic for resilience
* 🔌 Modular and scalable architecture
* 🐳 Fully containerized and reproducible

---

## 📚 Project Links

* Dataset: https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k
* Demo Video: https://drive.google.com/file/d/1HbTVXW3YuX7w2Z4ZMJYFX2QbSTGLFdvm/
  
---

## 👩‍💻 Author

**Zukhrahon Gulomova**
<br>Applied Artificial Intelligence, IU International University
