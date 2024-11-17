from fastapi import FastAPI ,Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from firebase_admin import credentials, initialize_app, db
from fastapi.responses import JSONResponse

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "hackathon-8d0fa",
  "private_key_id": "ef1d99cf548a3015d791a245bba90de680b3e774",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqfGaNusC5oZro\nbtMEeDo7LmgINPjL/SLKNMv2VVwYHw0ovDkEb1YeuqjYsBu/ehki0XQCH5Z7F2kz\nl8aTx2vCeBQShOmU9R/GlfVW39H7TOQv437L2pL0ncl210k5MMHlI+1hyU5qdyo8\nQIM3JB/BCT/3duUu8YY2XtO0R7MpYG7Nemc6cCmuAbiyMCAlRMDju4Ir6EvhCo6x\nH0dm+cpdZ6qYxgp7XmnbhvrjtFFskXe8K0jLK+An7/XZyBzjpPIDeOD+KDw8XaOk\nAO8EHEDqPv4HoyH6WoaJDgTGMn2RKXgLgIF6gwwpXzJrAXzDyiHKnvUiWSplnE7b\nhSK/Rf91AgMBAAECggEACKwc1GNWV+sIVAAFNHJANg/5g0dci5XkHeibInv7nA+C\nThrrBJZ8SUJiAenNc4tMuYhxkAUW1MqfU5xKIezQRrtwe/OuZSEl/WZV7VYj2pZx\n+hymr8x90rsvCyBO7X2VM2iFNAb3OfO3XorCkfzAr8NecWJnLKDlHKFsv/wwuS9E\n5pfnKMPRZBxrpvQOf+hZqdcwg0Kyt2GMM3m25LpSeGIr2qzl1ZDo5RHZf7hpFOdJ\nyT0GxM9wCbt8g01SPpycqjxZYvJjW8XCtEbXNs4ZSJbvXpSxd7r+w5gdWJTWk4Xn\nvRjcmj8B3VhL6IbopSVbYlcPhJ/2/wH2V2u40/ZpYQKBgQDv2HgRXEGqGQ1RJHDi\ngaMwtPlApLhSARdEQE6xFH2FKU4HFSlOav0MVnFddelQYCDvoDbW3cx888Ei9A9+\nlk9XanpTiij0UqeYV+PnJVo2vlZyOgUlmRnrwXdG6Nisuvsh1tQw8K3zZSGrd6dz\nDz9el2Pg9ZqMX4zftvhoOD311QKBgQC19//0aHHLDZZzT/P/2EhO4IBhjbLKUPcu\nfLlKl5SKQryvVRinhnwDu/iGe3zik7wsw9VEf8H1qyEd+ekboRDumUzoY3xAxz4F\nw/rSQl6W4B5hG0RApwTwWw4PMJjAqemqgJKc5e8exH8p2xSu1ruZUKVPXa47gPKD\n09t6LqCTIQKBgQDIcQ4W5BT0hK8+asf0ZAbvw66yuXZZAhRhs6SQFOG5kYVmIec9\nY+hKkUt4ofv0cgHUgP6TnxUwL73u6iywzAlOsuu8OTB0z0bE6F7MY8j7CyLPn3GB\ntGuXPT3jguDhqfoKk7ENnXaifJgg5oSIgeuhr7+G13rraUcgB5ed8bLGaQKBgQCj\n6DdNV6boV9zlEWefVJoNMntxY8lgI34DCaV9YvwRbfu3ktcaTzD1zCMYP7NGA/zD\n9cHsaYe0WekCr1Eh6frucHet+664Sr+7QcR0EARTspyqq3zXH5p7Rglr9UIiiOpJ\nAncNjK/O7v/8G7KNqi5g8xt0WdXPE19fDz3q2IUbAQKBgAeCm3+VWmYm6K5vXA/g\n5gOm2o+yJe4gccUfFLoOdMLWHek3QboFGXDYHPx/LbePFtq0+lHbURZRquCItpc8\nnwVpfuIDVWwqqO2cyi9QPkd56ssj87Y85mSIZMvE0u7xuByhZ5V9lWORlBNBkRvg\najl07LkFyz9y6S6VQukuqygr\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-pbyfu@hackathon-8d0fa.iam.gserviceaccount.com",
  "client_id": "113542427700727811206",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pbyfu%40hackathon-8d0fa.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)  # Replace with your Firebase Admin SDK JSON path
firebase_app = initialize_app(cred, {
    'databaseURL': 'https://hackathon-8d0fa-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})


app = FastAPI()

# Custom OpenAPI schema function
def custom_openapi():
    if not app.openapi_schema:
        openapi_schema = get_openapi(
            title="Your App Title",
            version="1.0.0",
            description="Your app description",
            routes=app.routes,
        )
        # Change OpenAPI version
        openapi_schema["openapi"] = "3.0.0"  # Ensure compatibility with tools expecting OpenAPI 3.0.0

        # Add servers field
        openapi_schema["servers"] = [{"url": "http://127.0.0.1:8000", "description": "Local server"}]

        # Check and remove ValidationError-related schemas and references
        if "components" in openapi_schema and "schemas" in openapi_schema["components"]:
            schemas = openapi_schema["components"]["schemas"]
            schemas.pop("ValidationError", None)  # Remove ValidationError schema if present
            schemas.pop("HTTPValidationError", None)  # Remove HTTPValidationError schema if present

        # Remove responses that reference ValidationError schemas
        for path, methods in openapi_schema["paths"].items():
            for method, details in methods.items():
                if "responses" in details:
                    for status_code, response in details["responses"].items():
                        if (
                            isinstance(response, dict)
                            and "content" in response
                            and "application/json" in response["content"]
                            and "schema" in response["content"]["application/json"]
                        ):
                            schema = response["content"]["application/json"]["schema"]
                            # Check if it references ValidationError schemas
                            if "$ref" in schema and any(
                                ref in schema["$ref"]
                                for ref in ["ValidationError", "HTTPValidationError"]
                            ):
                                # Replace with a generic response
                                response["content"]["application/json"]["schema"] = {"type": "object"}

        app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override the default OpenAPI schema function
app.openapi = custom_openapi

# Route to accept user_id and password
@app.post("/login/")
async def login(user_id: str):
    """
    Login endpoint that takes a user ID and password.
    """
    if user_id == "admin":
        return HTMLResponse(content=open("dashboard.html", "r").read())
    else:
        
        return {"status": "error", "message": "Invalid credentials"}
    


# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    html_path = os.path.join(os.getcwd(), "index.html")
    with open(html_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@app.get("/salary_page", response_class=HTMLResponse)
async def serve_html():
    return HTMLResponse(content=open("salary.html", "r").read())


@app.get("/dashboard", response_class=HTMLResponse)
async def serve_html():
    return HTMLResponse(content=open("dashboard.html", "r").read())

@app.get("/worker_data", response_class=JSONResponse)
async def worker_data():
    try:
        ref = db.reference('/Company A/Worker')
        data = ref.get()
        # Filter out null entries
        cleaned_data = [item for item in data if item is not None]
        return JSONResponse(content=cleaned_data)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)



@app.post("/salary_priority_algo/")
async def chat(request: Request):
    data = await request.json()
    l=["Base Salary","Working Hours","leaves taken","Manager Satisfaction"]
    algo=[]
    
    for i in data.key():
        algo.append(l.index(i))
    ref=db.reference('/Company A/Salary_Algo')
    ref.set(algo)

