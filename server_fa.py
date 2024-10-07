#pip install fastapi uvicorn bcrypt python-multipart gradio
from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import gradio as gr

app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Example hashed password for the user
hashed_password = pwd_context.hash("your_secure_password")

# Single user credentials (can be extended for multiple users)
fake_users_db = {
    "username": {
        "username": "admin",
        "hashed_password": hashed_password,
    }
}

# Gradio Interface Example
def chatbot_interface(user_input):
    return f"Hello {user_input}, welcome to the chatbot!"

gradio_app = gr.Interface(
    fn=chatbot_interface,
    inputs="text",
    outputs="text",
    title="Secure Chatbot"
)

# Simulating Gradio being hosted on /gradio
@app.get("/gradio")
def serve_gradio():
    gradio_app.launch(share=False, inline=False)

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get("username")
    if user and user["username"] == username:
        if verify_password(password, user["hashed_password"]):
            return user
    return None

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Successful login redirects to Gradio interface
    return RedirectResponse(url="/gradio", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/")
async def root():
    return {"message": "Go to /login to access the chatbot."}
