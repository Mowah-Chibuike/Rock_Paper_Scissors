# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates

# router = APIRouter(tags=["authentication"])
# templates = Jinja2Templates(directory="templates")

# Simple in-memory storage (replace with database for production)
# users = {}
isLoggedIn = False
current_user_id = None


# @router.get("/login", response_class=HTMLResponse)
# def login_page(request: Request):
#     """Display login page"""
#     return templates.TemplateResponse("login.html", {"request": request})


# @router.post("/login", response_class=HTMLResponse)
# async def login(request: Request):
#     """Handle user login"""
#     global isLoggedIn, current_user

#     form_data = await request.form()
#     email = form_data.get("email", "").strip()
#     password = form_data.get("password", "")

#     # Check if user exists and password is correct
#     if email in users and users[email]["password"] == password:
#         isLoggedIn = True
#         current_user = email
#         return RedirectResponse(url="/play/game", status_code=302)

#     return templates.TemplateResponse(
#         "login.html",
#         {
#             "request": request,
#             "error": "Invalid email or password",
#         },
#         status_code=401,
#     )


# @router.get("/register", response_class=HTMLResponse)
# def register_page(request: Request):
#     """Display registration page"""
#     return templates.TemplateResponse("register.html", {"request": request})


# @router.post("/register", response_class=HTMLResponse)
# async def register(request: Request):
#     """Handle user registration"""
#     global isLoggedIn, current_user

#     form_data = await request.form()
#     username = form_data.get("username", "").strip()
#     email = form_data.get("email", "").strip()
#     password = form_data.get("password", "")
#     confirm_password = form_data.get("confirm_password", "")

#     # Validate input
#     error = None

#     if not username or len(username) < 3 or len(username) > 20:
#         error = "Username must be between 3 and 20 characters"
#     elif not email:
#         error = "Email is required"
#     elif len(password) < 6:
#         error = "Password must be at least 6 characters"
#     elif password != confirm_password:
#         error = "Passwords do not match"
#     elif email in users:
#         error = "Email already registered"

#     if error:
#         return templates.TemplateResponse(
#             "register.html",
#             {
#                 "request": request,
#                 "error": error,
#             },
#             status_code=400,
#         )

#     # Create new user
#     users[email] = {
#         "username": username,
#         "password": password,
#         "email": email,
#     }

#     # Auto login after registration
#     isLoggedIn = True
#     current_user = email

#     return RedirectResponse(url="/play/game", status_code=302)


# @router.get("/logout")
# def logout():
#     """Handle user logout"""
#     global isLoggedIn, current_user
#     isLoggedIn = False
#     current_user = None
#     return RedirectResponse(url="/", status_code=302)