# ChatGPT Email Campaign Calendar Generator

## .env Configuration

The `.env` file is used for configuration settings. Follow these steps to set up your environment:

1. **API Key**: Add your OpenAI API key to the `.env` file by setting the variable `KEY`. This key is required for communication with the OpenAI API.

    ```env
    KEY=your_openai_api_key
    ```

2. **Origin Configuration**: Set the variable `ORIGIN` to specify your domain. This is crucial for security considerations.

    ```env
    ORIGIN=http://yourdomain.com
    ```

3. **Mode Selection**: The variable `MODE` determines the operating mode. Set it to `'PROD'` for production. For development purposes, set it to `"DEV"`.

    ```env
    MODE=PROD
    ```

## WSGI Server (Waitress)

This application uses Waitress as the WSGI server. Waitress is licensed under the Zope Public License (ZPL), a permissive open-source license.

## Running the Application

To run the application, follow these steps:

1. **Create a Python Virtual Environment**: Execute the following commands to create and activate a virtual environment:

    ```bash
    python -m venv venv
    ```

    - For Windows:

        ```bash
        venv\Scripts\activate
        ```

    - For Linux:

        ```bash
        source venv/bin/activate
        ```

2. **Install Dependencies**: Install the required packages from the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**: Navigate to the `ChatGPT` directory in your command prompt or VSCode terminal (where you activated the virtual environment) and execute:

    ```bash
    python app.py
    ```

## API Documentation

### Base URL
http://127.0.0.1:5000

### Endpoint
/prompt/

### Method

- **POST**

### Request

#### Headers

- Content-Type: application/json

#### Body

```json
{
    "shop_categories": "Clothing",
    "ccn": "Seasonal Discounts",
    "seasonality": "Spring",
    "ked": "Black Friday",
    "iskd": "Fashion Week",
    "shop_locations": "Online, New York"
}
```
  
### Response
Success
Status Code: 200 OK
```json 
{
    "response": "Generated email campaign calendar content."
}
```

Error
Status Code: 500 Internal Server Error
```json 
{
    "error": "An unexpected error occurred: Error details here."
}
```

## EXAMPLE

```bash 
curl -X POST -H "Content-Type: application/json" -d '{
    "shop_categories": "Clothing",
    "ccn": "Seasonal Discounts", //Content concept and narrative
    "seasonality": "Spring",
    "ked": "Black Friday", //Key E-commerce Dates
    "iskd": "Fashion Week", //Industry-Specific Key Days
    "shop_locations": "Online, New York"
}' http://127.0.0.1:5000/prompt/

```
