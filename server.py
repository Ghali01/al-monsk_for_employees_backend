import uvicorn
from staff_server.asgi import application
def serve():
    conf=uvicorn.Config(app=application,host='0.0.0.0',port=8000)
    server=uvicorn.Server(conf)
    server.run()
    
if __name__=='__main__':
    serve()