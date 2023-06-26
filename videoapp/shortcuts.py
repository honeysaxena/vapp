from videoapp.config import settings
from videoapp.database import session
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates 
from starlette.exceptions import HTTPException as StarletteHTTPException


templates = Jinja2Templates(directory=str(settings.templates_dir))

def is_htmx(request: Request):
    return request.headers.get("hx-request") == 'true'

def get_object_or_404(KlassName,  **kwargs):
    #session = SessionLocal()
    q = None
    try:
        query = session.query(KlassName).filter_by(**kwargs)

        #q = session.get(KlassName, **kwargs)
    except:
        raise StarletteHTTPException(status_code=404)
    #session.close()
    for q in query:
        return q
        
    #session.close()    
    #return q    

def redirect(path, cookies: dict={}, remove_session=False):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)
    if remove_session:
        response.set_cookie(key='session_ended', value=1, httponly=True)    
        response.delete_cookie('session_id')
    return response    


def render(request, template_name, context:dict={}, status_code: int = 200, cookies:dict={}):

    ctx = context.copy()
    ctx.update({"request": request})
    t = templates.get_template(template_name)
    html_str = t.render(ctx)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(cookies.keys()) > 0:
        response.set_cookie(key='darkmode', value=1)
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    #print(request.cookies)  
    #for key in request.cookies.keys():
    #    response.delete_cookie(key)
    return response
    #return templates.TemplateResponse(template_name, ctx, status_code=status_code)




