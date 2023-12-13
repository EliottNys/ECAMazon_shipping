# ECAMazon_shipping

This microservice manages sent and returned parcels and their complete traceability.

[DockerHub repository](https://hub.docker.com/r/nislhin/ecamazon_shipping)

To test locally, use the following commands:
```bash
docker-compose build
docker-compose up
```

## API Endpoints

### Search Parcel by ID

Search a parcel by Parcel, Order or User ID.

- **URL**: `/`
- **Method**: `GET`
- **Response**:
  - **Success (200 OK)**: html page

### Retrieve Parcel Information

Retrieve information about a specific parcel.

- **URL**: `/parcel/<parcel_id>`
- **Method**: `GET`
- **Parameters**:
  - `parcel_id` (integer): The unique identifier for the parcel.
- **Response**:
  - **Success (200 OK)**: HTML page
  - **Error (404 Not Found)**:
    ```json
    {
        "error": "Parcel not found"
    }
    ```

### Retrieve All Parcels

Retrieve information about all parcels.

- **URL**: `/all_parcels`
- **Method**: `GET`
- **Parameters**:
  - `page` (integer, optional): The page number for pagination (default is 1).
- **Response**:
  - **Success (200 OK)**: HTML page
  - **Error (500 Internal Server Error)**:
    ```json
    {
        "error": "Internal Server Error"
    }
    ```

### Retrieve Users's Parcels

Retrieve information about all parcels.

- **URL**: `/user/<user_id>`
- **Method**: `GET`
- **Parameters**:
  - `user_id` (integer): The unique identifier for the user
  - `page` (integer, optional): The page number for pagination (default is 1).
- **Response**:
  - **Success (200 OK)**: HTML page
  - **Error (404 Not Found)**:
    ```json
    {
        "error": "User not found"
    }
    ```
  - **Error (500 Internal Server Error)**:
    ```json
    {
        "error": "Internal Server Error"
    }
    ```

### Retrieve Order's Parcels

Retrieve information about all parcels.

- **URL**: `/order/<order_id>`
- **Method**: `GET`
- **Parameters**:
  - `order_id` (integer): The unique identifier for the order
  - `page` (integer, optional): The page number for pagination (default is 1).
- **Response**:
  - **Success (200 OK)**: HTML page
  - **Error (404 Not Found)**:
    ```json
    {
        "error": "Order not found"
    }
    ```
  - **Error (500 Internal Server Error)**:
    ```json
    {
        "error": "Internal Server Error"
    }
    ```

### Create a New Parcel (STOCK microservice)

Create a new parcel with the provided data.

- **URL**: `/new_parcel`
- **Method**: `POST`
- **Parameters**:
  - `order_id` (integer): The unique identifier for the order.
  - `user_id` (integer): The unique identifier for the user.
  - `parcel_id` (integer): The unique identifier for the parcel.
- **Request Body**:
  ```json
  {
      "order_id": 123,
      "user_id": 456,
      "parcel_id": 789
  }
- **Response**:
  - **Success** (200 OK)**:
    ```json
    {
    "message": "Parcel information received successfully"
    }
    ```

### Update Parcel Status (DISPATCHING microservice)

Update the status of a specific parcel.

- **URL**: `/update_status`
- **Method**: `POST`
- **Parameters**:
  - `parcel_id` (integer): The unique identifier for the parcel.
  - `status` (string) : The new status of the parcel
- **Request Body**:
  ```json
  {
      "parcel_id": 123,
      "status": "Delivered"
  }
  ```
- **Response**:
  - **Success** (200 OK)**:
    ```json
    {
    "message": "Parcel status updated successfully"
    }
    ```
  - **Error (404 Not Found)**:
    ```json
    {
        "error": "Parcel not found"
    }
    ```
  - **Error (400 Bad Request)**:
    ```json
    {
        "error": "Missing data"
    }
    ```