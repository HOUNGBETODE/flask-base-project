from commons.instances.instances import logger
from seeder.super_admin_seeder.adaptater import SuperAdminAdaptater

class SuperAdminScript:

    @staticmethod
    def run():
        if not SuperAdminAdaptater.check_existing_super_admin():
            if SuperAdminAdaptater.create_super_admin():
                logger.info("Successfully created super admin user")
        else:
            logger.info(f"Found existing super admin user")
