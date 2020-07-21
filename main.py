from sanic import Sanic

from setup import db, Settings

app = Sanic(__name__, log_config=Settings.get_log_config())

from files_app.routes import bp

app.blueprint(bp)


@app.listener('after_server_start')
async def connect_to_db(*args, **kwargs):
    await db.connect()


@app.listener('after_server_stop')
async def disconnect_from_db(*args, **kwargs):
    await db.disconnect()


if __name__ == '__main__':
    app.run(host=Settings.get_host(), port=Settings.get_port(), debug=True)
