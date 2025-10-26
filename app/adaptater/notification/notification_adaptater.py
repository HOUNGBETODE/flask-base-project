from flask import Flask
from commons.instances.instances import logger
from data.entities.config.entities_config import db
from concurrent.futures import ThreadPoolExecutor, as_completed
from data.entities.notification.notification import Notification


class NotificationAdaptater:

    @staticmethod
    def create_notification(app: Flask, title:str, message: str, tag: str, user_id: str = None):
        from adaptater.user.user_adaptater import UserAdaptater
        with app.app_context():
            try:
                user = UserAdaptater.get_by_id(user_id) if user_id else None

                if user:
                    new_notification = Notification(
                        user_id=user.id,
                        title=title,
                        message=message,
                        tag=tag,
                        unread=True
                    )

                    db.session.add(new_notification)
                    db.session.commit()

                    return new_notification.to_dict()

            except Exception as e:
                db.session.rollback()
                logger.error(f"Error in create_notification function adaptater: {e}")
                raise e
    

    @staticmethod
    def create_batch_notification(app: Flask, title: str, message: str, tag: str):
        from data.entities.user.user import User
        with app.app_context():
            try:
                users = db.session.query(User).filter(
                    User.is_verified == True,
                    User.is_deleted == False,
                    User.is_active == True
                ).all()

                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(
                        NotificationAdaptater.create_notification,
                        app,
                        title,
                        message,
                        tag,
                        user.id,
                    ) for user in users]

                    results = []

                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                        except Exception as e:
                            logger.error(f"Batch notification failed for a user: {e}")
                    
                    return results

            except Exception as e:
                db.session.rollback()
                logger.error(f"Error in create_batch_notification function adaptater : {e}")
                raise e
    

    @staticmethod
    def get_unread_count(user_id: str) -> int:
        try:
            unread_count = db.session.query(Notification).filter_by(user_id=user_id, unread=True).count()
            return unread_count
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in get_unread_notifications_count function adaptater: {e}")
            raise e


    @staticmethod
    def get_unread_notifications(user_id: str, page: int = 1, per_page: int = 10):
        try:
            return db.session.query(Notification).filter_by(user_id=user_id, unread=True).order_by(Notification.created_at.desc()) \
                .paginate(page=page, per_page=per_page, error_out=False)
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in get_unread_notifications function adaptater: {e}")
            raise e


    @staticmethod
    def mark_notifications_as_read(user_id: str, target: str):
        try:
            if target == "all":
                db.session.query(Notification).filter_by(user_id=user_id, unread=True).update({"unread": False})
                db.session.commit()
            else:
                notification = db.session.query(Notification).filter_by(id=target, user_id=user_id, unread=True).first()
                if notification:
                    notification.unread = False
                    db.session.commit()
                else:
                    return False
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in mark_notifications_as_read function adaptater: {e}")
            raise e
