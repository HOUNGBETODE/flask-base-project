import os
from commons.instances.instances import logger
from data.entities.config.entities_config import db
from flask_migrate import Migrate, migrate, upgrade, init


def run_migrations(app):
    migrations_dir = 'migrations'
    migrate_instance = Migrate(app,db)

    # Check if migrations directory exists
    if not os.path.exists(migrations_dir):
        try:
            init()
            logger.info("Migration repository initialized.")
        except Exception as e:
            logger.error(f"Error initializing migration repository: {e}")
    else:
        logger.debug("Migration repository already exists.")

    # Generate migration scripts if needed
    try:
        logger.debug("Trying migrate")
        migrate()
        logger.info("Migration scripts generated.")
    except Exception as e:
        logger.error(f"Error generating migration scripts: {e}")

    # Apply migrations
    try:
        upgrade()
        logger.info("Database migrations applied successfully.")
    except Exception as e:
         logger.error(f"Error applying migrations: {e}")
