from app.routers.routers import BaseView
from app.create_app.create import app


if __name__ == '__main__':
    BaseView.register(app)
    app.run(host='0.0.0.0')
