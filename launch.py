from flaskr import create_app
from gevent.pywsgi import WSGIServer
from instance.config import SERVER_PORT

import asyncio

async def run():

    app = create_app()
    server = WSGIServer(('0.0.0.0', SERVER_PORT), application=app)
    server.serve_forever()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run())
    
    except KeyboardInterrupt:
        print('Interrupted by user') 
    
    finally:
        loop.close()
