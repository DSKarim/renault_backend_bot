# 🚗 MyRenault API Backend

A generic, stateless FastAPI backend for controlling Renault electric vehicles (ZOE, Megane E-Tech, Twingo ZE, etc.) via the unofficial My Renault API.

This project wraps the [renault-api](https://github.com/hacf-fr/renault-api) library into a RESTful API, designed to serve mobile applications (like the [planned Android App](PLAN_ANDROID.md)), dashboards, or home automation systems.

## ✨ Features

- **🔋 Battery Status**: Get battery level (%), autonomy (km), charging status, and plug status.
- **🛣️ Cockpit**: Retrieve total mileage.
- **📍 Location**: Get the vehicle's GPS position (latitude, longitude).
- **🌡️ HVAC Control**: Start (with temperature) or stop air conditioning/heating.
- **⚡ Charge Control**: Start or cancel charging.
- **🔔 Alerts**: Blink lights or honk (to find the vehicle).
- **🔒 Multi-User**: Stateless architecture allows any user to connect by providing credentials in request headers.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- A valid My Renault account (Email & Password)
- Your Vehicle Identification Number (VIN)

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/myrenault-api.git
    cd myrenault-api
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the server:**
    ```bash
    uvicorn api:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### Docker Deployment

1.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```

2.  **Verify:**
    Check the logs to ensure the server is running:
    ```bash
    docker-compose logs -f
    ```

## 📖 API Usage

The API uses **Headers** for authentication. You must provide your Renault credentials with every request. This allows the backend to be stateless and support multiple users.

**Required Headers:**
- `x-renault-email`: Your My Renault email address.
- `x-renault-password`: Your My Renault password.

*(Note: You can also set `RENAULT_EMAIL` and `RENAULT_PASSWORD` as environment variables for a default fallback, useful for single-user deployments).*

### Examples

#### 1. Get Battery Status
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/vehicle/YOUR_VIN/battery' \
  -H 'accept: application/json' \
  -H 'x-renault-email: your.email@example.com' \
  -H 'x-renault-password: your_password'
```

#### 2. Start HVAC (Air Conditioning)
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/vehicle/YOUR_VIN/hvac-start?temp=21' \
  -H 'accept: application/json' \
  -H 'x-renault-email: your.email@example.com' \
  -H 'x-renault-password: your_password'
```

#### 3. Get Location
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/vehicle/YOUR_VIN/location' \
  -H 'accept: application/json' \
  -H 'x-renault-email: your.email@example.com' \
  -H 'x-renault-password: your_password'
```

## 🗺️ Roadmap

### ✨ Features
- [ ] **Android Application**: A native Android app is planned to consume this API. See [PLAN_ANDROID.md](PLAN_ANDROID.md) for details.
- [ ] **Wear OS Support**: Companion app for smartwatches.
- [ ] **Charging Schedule**: Ability to set charging schedules via API.
- [ ] **Notifications**: Push notifications for battery levels (via Firebase).

### 🛠️ Technical Improvements
- [ ] **Env Var Fallback**: Implement optional headers if environment variables are set (fix discrepancy).
- [ ] **CI/CD Pipeline**: Add GitHub Actions for linting and testing.
- [ ] **Test Coverage**: Add more unit tests for error scenarios (timeouts, upstream errors).
- [ ] **Session Caching**: Reuse Renault API sessions to improve performance and reduce login requests.
- [ ] **Structured Logging**: Replace standard logging with structured JSON logging for better observability.

## ⚠️ Disclaimer

This project uses an **unofficial API** from Renault. It may change or break at any time without notice. Use this software at your own risk. The developers are not affiliated with Renault.
