#pip install fastapi uvicorn bcrypt python-multipart gradio
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.sessions import SessionMiddleware
import httpx
from passlib.context import CryptContext
import gradio as gr
import threading
import sim_bot

app = FastAPI()

# Add session middleware for handling sessions (in-memory storage)
app.add_middleware(SessionMiddleware, secret_key="my_secret_pass", max_age=3600)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Single user credentials (can be extended for multiple users)
fake_users_db = {
    "username": {
        "username": "cool_user",
        "hashed_password": "$2b$12$pL2x75EjYsDR8ardKI/hL.VYSSk9s/unfJNFw3jaMXrdk1/gIC/Qq",
    }
}

#=============================================================================================
# Gradio Interface Example
def chatbot_interface(user_input):
    return f"Hello {user_input}, welcome to the chatbot!"

#gradio_app = gr.Interface(
#    fn=chatbot_interface,
#    inputs="text",
#    outputs="text",
#    title="Secure Chatbot"
#)

gradio_app = gr.Interface(
    fn=sim_bot.process_query,
    inputs="text",
    outputs="text",
    title="Secure Chatbot"
)


# Launch Gradio in a separate thread to prevent blocking FastAPI
def launch_gradio():
    gradio_app.launch(share=False, server_name="0.0.0.0", server_port=7860, inline=False)
#    with gr.Blocks() as iface:
#        chatbot = gr.ChatInterface(
#            fn=process_query,
#            title="Simulation Creation Assistant",
#            description="A helpful assistant for creating INI files",
#            chatbot=gr.Chatbot(height=600),
#            retry_btn=None,
#            undo_btn=None,
#            clear_btn=None,
#        )
#        iface.launch(share=False, server_name="0.0.0.0", server_port=7860, inline=False)

thread = threading.Thread(target=launch_gradio)
thread.start()    

#=============================================================================================

# Protect /gradio route
def get_current_user(request: Request):
    if "user" not in request.session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return request.session['user']

#=============================================================================================
@app.get("/gradio", response_class=HTMLResponse)
async def serve_gradio(request: Request, user: str = Depends(get_current_user)):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot Interface</title>
    </head>
    <body>
        <h2>Welcome to the Secure Chatbot</h2>
        <iframe src="http://0.0.0.0:7860?__theme=dark" width="100%" height="800"></iframe>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
#=============================================================================================

# Serve login form as HTML on GET request
@app.get("/login", response_class=HTMLResponse)
async def login_form():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h2>Login Form</h2>
        <form action="/login" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br><br>
            
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Process login form submission (POST request)
@app.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Store user session
    request.session['user'] = form_data.username
    
    # Successful login redirects to the Gradio interface at port 7860
    #return RedirectResponse(url="http://127.0.0.1:7860?__theme=dark", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse(url="/gradio", status_code=status.HTTP_303_SEE_OTHER)


# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get("username")
    if user and user["username"] == username:
        if verify_password(password, user["hashed_password"]):
            print("Successful authentication")
            return user
    return None

@app.get("/")
async def root():
    return {"message": "Go to /login to access the chatbot."}
