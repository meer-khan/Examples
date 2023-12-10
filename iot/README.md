# Flask API for IoT Data Management

This Flask API provides endpoints for managing IoT data, including user information and data records. It uses Waitress as the WSGI server and requires a Python virtual environment.

## Environment Variables (.env)

Add the following keys to your `.env` file:

- `PORT`: Port of the database.
- `ORIGIN`: Your domain.
- `MODE`: Set to 'PROD' for production, or 'DEV' for development.

## Running the Application

1. Create a Python virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - For Windows:

    ```bash
    venv\Scripts\activate
    ```

    - For Linux:

    ```bash
    source venv/bin/activate
    ```

3. Install packages from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. Navigate to the `iot` directory:

    ```bash
    cd iot
    ```

5. Run the application:

    ```bash
    python app.py
    ```

## API Documentation

### BASE URL

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Endpoints

- `/user/`
- `/adduser/`

## Methods

- `POST`
- `GET`

## Request Headers

- `Content-Type: application/json`

## Request Body Example

```json
{
  "userID": "",
  "location": "Lahore, Hall Road",
  "noOfPeople": 100,
  "totalTraffic": 10,
  "totalMale": 90,
  "totalFemale": 140,
  "totalKids": 10
}  
```
## INSTRUCTIONS:   
    >> /user/ , use GET method to get all users data 
    >> /addusers/, use POST method to add a user in the database with following parameters 
```json
    {
    "brandName": "",
    "email": "", 
    "password": , 
    "location": ""
    }
```
    >> /users/, use POST method to add data in the "Data" collection with the following parameters
```json
    {
    "userID": "65760b7dd8be27567528f722",
    "location": "", 
    "noOfPeople": 100,
    "totalTraffic": 10,
    "totalMale":90,
    "totalFemale":140,
    "totalKids":10 
    }
```
**NOTE**: Use the exact user id (given above) to add the data in the database