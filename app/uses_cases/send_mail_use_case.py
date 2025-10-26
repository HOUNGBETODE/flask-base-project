from flask import Flask
from data.entities.user.user import User
from commons.utils.utils import geolocate_ip
from commons.helpers.load_doten import Dotenv
from commons.instances.instances import logger
from adaptater.user.user_adaptater import UserAdaptater
from services.smtp_function.send_mail import EmailService
from commons.enums.user_genders.genders import UserGender


email_service = EmailService()

class SendMail:

    @staticmethod
    def send_one_mail(app: Flask, email: str, subject: str, mail_message: str, verification_code: str | None, email_type: str):
        with app.app_context():
            email_service.send_email(email, subject, mail_message, verification_code, email_type)


    @staticmethod
    def send_login_notification(app: Flask, user: User, device_info: dict = None) -> bool:
        with app.app_context():
            try:
                user_civility = "M. " if (user.gender == UserGender.MALE.value) else "Mme/Mlle " if (user.gender == UserGender.FEMALE.value) else ""
                user_name = f"{user_civility}{user.lastname} {user.firstname}"
                device_str = ""
                
                if device_info:
                    remote_ip = device_info.get('remote_ip', 'Non spécifiée')
                    device_info['location'] = geolocate_ip(remote_ip)

                    device_str = f"<p><strong>Appareil :</strong> {device_info.get('device', 'Non spécifié')}<br>"
                    device_str += f"<strong>Localisation :</strong> {device_info.get('location', 'Non disponible')}</p>"
                
                subject = "🔐 Nouvelle connexion à votre compte"
                message = f"""
                    <h2 style="color: #2c2c2c; margin-bottom: 20px;">Connexion détectée</h2>
                    <p>Bonjour {user_name},</p>
                    <p>Une nouvelle connexion à votre compte a été détectée.</p>
                    {device_str}
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-top: 30px;">
                        <p style="margin-top: 30px;"><strong>⚠️ Ce n'était pas vous ?</strong></p>
                        <p style="margin-left: 20px; color: #2c2c2c;">
                            Si vous ne reconnaissez pas cette connexion, veuillez immédiatement :
                        </p>
                        <ul style="margin-left: 40px; color: #2c2c2c;">
                            <li>Changer votre mot de passe</li>
                            <li>Contacter notre support</li>
                            <li>Vérifier l'activité de votre compte</li>
                        </ul>
                    </div>
                """

                return email_service.send_email(user.email, subject, message, None, "login_notification")
                
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de la notification de connexion pour {user.email}: {str(e)}")
                raise e
