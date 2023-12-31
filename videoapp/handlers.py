from starlette.exceptions import HTTPException as StarletteHTTPException

from videoapp.main import app
from videoapp.shortcuts import render, redirect, is_htmx
from videoapp.users.exceptions import LoginRequiredException

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = 'errors/main.html'
    context  = {"status_code": status_code}
    return render(request, template_name, context, status_code=status_code)


@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exc):
    response = redirect(f"/login?next={request.url}", remove_session=True)
    if is_htmx(request):
        response.status_code = 200
        response.headers['HX-Redirect'] = "/login"
    return response