from flask_migrate import Migrate
from commons.config.config.config import Config
from core.dependance.dependance import create_app
from data.entities.config.entities_config import db
from seeder.super_admin_seeder.script import SuperAdminScript
from commons.migrations_init.migrate_app import run_migrations


app = create_app()

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    run_migrations(app)

    SuperAdminScript.run()


if __name__ == "__main__":
    # Run application
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
