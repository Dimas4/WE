from app.routers.routers import BaseView
from app.database.model import *


if __name__ == '__main__':
    BaseView.register(app)
    app.run(host='0.0.0.0', port=8000)
