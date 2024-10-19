from celery import Celery, Task
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

broker_url = "amqp://guest:guest@rabbitmq:5672/final_project"
db_url = "postgresql+psycopg2://thanhnt:thanhnt@postgres:5432/final_project"
# db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=broker_url,
            result_backend="rpc://",
            task_ignore_result=True,
        ),
    )
    # db.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config['SQLALCHEMY_POOL_SIZE'] = 10  # Adjust as needed
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30  # Adjust as needed
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 20,  # Increase the pool size
        'max_overflow': 10,  # Allow overflow connections
    }
    # app.config.from_prefixed_env()
    celery_init_app(app)
    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
