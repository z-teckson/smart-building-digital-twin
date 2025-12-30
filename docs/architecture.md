# Smart Building Digital Twin – System Architecture

## Overview

The digital twin system is designed as a modular, event‑driven platform that mirrors a physical smart building in a virtual environment. It ingests real‑time sensor data, processes it through simulation and analytics models, and provides actionable insights for building operators.

## High‑Level Components

### 1. IoT Data Ingestion Layer
- **Purpose**: Collect sensor readings from the building’s IoT infrastructure (HVAC, lighting, occupancy, environmental sensors, etc.).
- **Components**:
  - **IoT Gateway**: A lightweight edge device that aggregates raw sensor data and forwards it to the cloud via secure protocols (MQTT, HTTP).
  - **Ingestion API**: A RESTful endpoint (`/api/v1/sensor-data`) that accepts JSON‑formatted sensor readings, validates them, and places them into a message queue (e.g., Apache Kafka, RabbitMQ).
- **Data Format**:
  ```json
  {
    "sensor_id": "temp_zone_101",
    "timestamp": "2025-01-15T14:30:00Z",
    "value": 22.5,
    "unit": "celsius",
    "metadata": {"floor": 1, "room": "101"}
  }
  ```

### 2. Data Processing Engine
- **Purpose**: Transform raw sensor data into structured events, detect anomalies, and prepare data for the digital twin model.
- **Components**:
  - **Stream Processor**: (e.g., Apache Flink, Spark Streaming) that applies real‑time transformations, filters, and enrichment.
  - **Anomaly Detector**: A lightweight ML model that flags unusual readings (e.g., sudden temperature spikes, zero‑occupancy during peak hours) and raises alerts.
  - **Data Store**: A time‑series database (e.g., InfluxDB, TimescaleDB) that stores cleaned, aggregated sensor data for historical analysis.

### 3. Digital Twin Model
- **Purpose**: Maintain a virtual representation of the building’s physical assets and their current state.
- **Components**:
  - **Asset Registry**: A catalog of all building assets (HVAC units, lighting fixtures, occupancy sensors) with their static properties (location, manufacturer, model).
  - **State Manager**: Updates the state of each asset based on incoming sensor events (e.g., `HVACSystem.current_temperature`, `LightingSystem.brightness_level`).
  - **Simulation Engine**: Runs “what‑if” scenarios (e.g., “What happens if we lower the setpoint by 2°C during the night?”) using a physics‑based or data‑driven model of the building’s thermal dynamics.
- **Core Classes** (defined in `src/asset_model.py`):
  - `HVACSystem`: Tracks temperature setpoint, current temperature, operational status.
  - `LightingSystem`: Tracks brightness level, occupancy status, energy consumption.

### 4. Analytics & Optimization Layer
- **Purpose**: Derive actionable insights and automated control commands from the twin’s state.
- **Components**:
  - **Energy Optimizer**: An algorithm that adjusts HVAC and lighting setpoints to minimize energy usage while respecting comfort constraints. It uses historical consumption patterns, real‑time occupancy, and weather forecasts.
  - **Comfort Monitor**: Evaluates the indoor environmental quality (temperature, humidity, CO₂, lighting) against predefined comfort bands and suggests corrective actions.
  - **Predictive Maintenance Module**: Applies failure‑prediction models to detect early signs of equipment degradation and schedules maintenance.

### 5. Visualization & Interface Layer
- **Purpose**: Present the twin’s state, analytics results, and control options to building operators.
- **Components**:
  - **Dashboard**: A web‑based UI (e.g., built with React/D3.js) that shows real‑time building metrics, energy consumption trends, and alerts.
  - **API Gateway**: Exposes REST and WebSocket endpoints for external systems (BMS, third‑party analytics) to query the twin’s state and submit control commands.
  - **Notification Service**: Sends email/SMS alerts when anomalies or maintenance events are detected.

## Data Flow

1. **Ingestion**: Sensor data → IoT Gateway → Ingestion API → Message Queue.
2. **Processing**: Message Queue → Stream Processor → Anomaly Detection → Time‑Series DB.
3. **Twin Update**: Processed events → State Manager → Digital Twin Model (asset state updated).
4. **Analytics**: Updated twin state → Energy Optimizer / Comfort Monitor → Generate recommendations.
5. **Visualization**: Twin state + recommendations → Dashboard / API Gateway → Operator.

## Deployment Considerations

- **Cloud‑Native**: The system is designed to run on a cloud platform (AWS, Azure, GCP) using containerized microservices (Docker, Kubernetes).
- **Edge Computing**: For low‑latency control, lightweight analytics modules can be deployed on edge gateways.
- **Security**: All communication channels use TLS encryption; device authentication is handled via certificates or API keys; access to the twin’s API is governed by role‑based access control (RBAC).

## Future Extensions

- Integration with external weather APIs for more accurate predictive control.
- Addition of renewable energy sources (solar panels, batteries) to the asset model.
- Machine‑learning‑based occupancy prediction to further optimize pre‑heating/cooling schedules.