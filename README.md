# Avito Academy of Analysts "Backend Development Basics"


# Plate Reader Service

This Flask application provides a service for reading license plate numbers from images using a pre-trained model. It also includes endpoints for greeting users and fetching images for processing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your/repository.git
   ```

2. Install dependencies:
   ```bash
   docker build -t ds-backend
   docker run  -t -v $PWD:/app -p 8080:8080 ds-backend
   ```

## Usage

1. The service will run on `http://localhost:8080`.

2. Endpoints:
   - `/greeting`: POST endpoint to greet a user.
   - `/readPlateNumber`: POST endpoint to read a license plate number from an image.
   - `/idToNum`: POST endpoint to read a license plate number from an image fetched by ID.
   - `/idToNumBatch`: POST endpoint to read license plate numbers from multiple images fetched by IDs.

## API Documentation

### Greeting
- **URL:** `/greeting`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "user": "username"
  }
  ```
- **Response:**
  ```json
  {
    "result": "Hello username"
  }
  ```

### Read Plate Number
- **URL:** `/readPlateNumber`
- **Method:** POST
- **Request Body:** Image bytes
- **Response:**
  ```json
  {
    "plate_number": "license_plate_number"
  }
  ```

### ID to Number
- **URL:** `/idToNum`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "pict_id": "image_id"
  }
  ```
- **Response:**
  ```json
  {
    "plate_number": "license_plate_number"
  }
  ```

### ID to Number Batch
- **URL:** `/idToNumBatch`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "pict_ids": ["image_id1", "image_id2", ...]
  }
  ```
- **Response:**
  ```json
  {
    "plate_numbers": [
      {
        "pict_id": "image_id1",
        "plate_number": "license_plate_number1"
      },
      {
        "pict_id": "image_id2",
        "plate_number": "license_plate_number2"
      },
      ...
    ]
  }
  ```

  ### Error Responses
- **Status Code 400:**
  ```json
  {
    "error": "Invalid request format"
  }
  ```

- **Status Code 404:**
  ```json
  {
    "error": "Resource not found"
  }
  ```

- **Status Code 500:**
  ```json
  {
    "error": "Internal server error"
  }
  ```