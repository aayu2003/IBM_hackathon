from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
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
async def login(user_id: str, password: str):
    """
    Login endpoint that takes a user ID and password.
    """
    if user_id == "admin" and password == "secret":
        return {"status": "success", "message": "Welcome, admin!"}
    else:
        print("hogyisssss")
        return {"status": "error", "message": "Invalid credentials"}
    


# Serve the HTML file
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    html_path = os.path.join(os.getcwd(), "index.html")
    with open(html_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
