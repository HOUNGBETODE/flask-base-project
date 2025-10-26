import pyotp
from typing import Optional
from commons.helpers.load_doten import Dotenv
from commons.instances.instances import logger
from commons.config.config.config import Config
from commons.enums.user_genders.genders import UserGender
from services.smtp_function.send_mail import EmailService
from adaptater.user.user_adaptater import UserAdaptater, User


email_service = EmailService()

class UserUseCase:

    @staticmethod
    def forgot_password_code(email: str) -> Optional[str]:
        try:
            user = UserAdaptater.get_by_email(email)
            
            if not user:
                logger.warning(f"Tentative de réinitialisation pour un email inexistant: {email}")
                raise e

            password_reset_code = pyotp.TOTP(
                s=UserAdaptater.generate_password_reset_secret(user),
                digits=Config.OTP_DIGITS_NUMBER,
                interval=Config.OTP_EXPIRATION_TIMEOUT
            ).now()

            if email_service.send_password_reset_email(user.email, password_reset_code):
                logger.info(f"Code de réinitialisation envoyé à {email}")
                return password_reset_code
            else:
                logger.error(f"Échec de l'envoi du code de réinitialisation à {email}")
                raise e
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération du code de réinitialisation pour {email}: {str(e)}")
            raise e


    @staticmethod
    def resend_forgot_password_code(email: str) -> Optional[str]:
        try:
            user = UserAdaptater.get_by_email(email)

            if not user:
                logger.warning(f"Tentative de renvoi de code pour un email inexistant: {email}")
                raise e

            password_reset_code = pyotp.TOTP(
                s=UserAdaptater.generate_password_reset_secret(user),
                digits=Config.OTP_DIGITS_NUMBER,
                interval=Config.OTP_EXPIRATION_TIMEOUT
            ).now()
   
            subject = "🔐 Renvoi - Code de réinitialisation"
            message = """
                <h2 style="color: #2c2c2c; margin-bottom: 20px;">Renvoi du code de réinitialisation</h2>
                <p>Voici votre nouveau code de réinitialisation du mot de passe :</p>
                <p style="margin-top: 30px;"><strong>⏰ Rappel important :</strong></p>
                <ul style="margin-left: 20px; color: #2c2c2c;">
                    <li>Ce code remplace le précédent</li>
                    <li>Il expire dans 5 minutes</li>
                    <li>Utilisez-le rapidement pour réinitialiser votre mot de passe</li>
                </ul>
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-top: 30px;">
                    <p style="color: #856404; margin: 0; font-weight: 600;">
                        🛡️ <strong>Notice de sécurité :</strong>
                    </p>
                    <p style="color: #856404; margin-top: 10px; margin-bottom: 0; font-size: 14px; line-height: 1.6;">
                        Si vous n'êtes pas à l'origine de cette demande de réinitialisation, 
                        vous pouvez ignorer cet email en toute sécurité. Votre mot de passe actuel reste inchangé 
                        et votre compte demeure protégé.
                    </p>
                </div>
            """
            
            if email_service.send_email(user.email, subject, message, password_reset_code, "password_reset_resend"):
                logger.info(f"Code de réinitialisation renvoyé à {email}")
                return password_reset_code
            else:
                logger.error(f"Échec du renvoi du code de réinitialisation à {email}")
                raise e
                
        except Exception as e:
            logger.error(f"Erreur lors du renvoi du code de réinitialisation pour {email}: {str(e)}")
            raise e
    

    @staticmethod
    def send_admin_verification_code(email: str) -> Optional[str]:
        try:
            user = UserAdaptater.get_by_email(email)

            if not user:
                logger.warning(f"Tentative d'envoi de code de vérification pour un email inexistant: {email}")
                raise e

            identity_verification_code = pyotp.TOTP(
                s=UserAdaptater.generate_account_activation_secret(user),
                digits=Config.OTP_DIGITS_NUMBER,
                interval=Config.OTP_EXPIRATION_TIMEOUT
            ).now()
    
            subject = "🔐 Code de vérification"
            message = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                    <h1 style="color: #2c2c2c; text-align: center; margin-bottom: 20px;">Bonjour {user.firstname or 'Utilisateur'},</h1>
                    <h2 style="color: #2c2c2c; margin-bottom: 20px; text-align: center;">Voici votre code de vérification</h2>
                    <p style="color: #2c2c2c; margin-bottom: 20px; text-align: center;">
                        Pour garantir la sécurité de votre compte, nous devons vérifier votre identité avant de poursuivre votre connexion.
                    </p>
                    <div style="text-align: center; margin: 40px 0;">
                        <h3 style="color: #2c2c2c; margin-bottom: 10px;">Code de vérification :</h3>
                        <div style="display: inline-block; background-color: #ffffff; border: 2px solid #dee2e6; border-radius: 8px; padding: 20px 40px; font-size: 24px; font-weight: bold; letter-spacing: 10px; color: #495057;">
                            {identity_verification_code}
                        </div>
                    </div>
                    <p style="color: #2c2c2c; text-align: center; margin-bottom: 20px;">
                        Ce code est valide pendant 10 minutes.
                    </p>
                    <p style="color: #2c2c2c; text-align: center; margin-bottom: 20px;">
                        Si le code expire, vous pouvez demander un nouveau code de vérification.
                    </p>
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px; margin-top: 30px;">
                        <p style="color: #856404; margin: 0; font-weight: 600; text-align: center;">
                            🛡️ <strong>Notice de sécurité :</strong>
                        </p>
                        <p style="color: #856404; margin-top: 10px; margin-bottom: 0; font-size: 14px; line-height: 1.6; text-align: center;">
                            Si vous n'êtes pas à l'origine de cette demande de connexion, 
                            vous pouvez ignorer simplement cet e-mail, votre compte reste protégé.
                        </p>
                        <p style="color: #2c2c2c; text-align: center; font-weight: bold; margin-bottom: 40px;">
                            L'équipe de Support
                        </p>
                    </div>
                </div>
            """
            
            if email_service.send_email(user.email, subject, message, identity_verification_code, "admin_verification"):
                logger.info(f"Code de vérification admin envoyé à {email}")
                return identity_verification_code
            else:
                logger.error(f"Échec de l'envoi du code de vérification admin à {email}")
                raise e
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du code de vérification admin pour {email}: {str(e)}")
            raise e
    

    @staticmethod
    def send_admin_welcome_email(username: str, email: str, temp_password: str) -> bool:
        try:
            subject = "Bienvenue dans l'équipe !"
            message = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                    <h1 style="color: #2c2c2c; text-align: center; margin-bottom: 20px;">Bonjour {username},</h1>
                    <h2 style="color: #2c2c2c; margin-bottom: 20px; text-align: center;">Bienvenue dans l'équipe !</h2>
                    <p style="color: #2c2c2c; margin-bottom: 20px; text-align: center;">
                        Un compte administrateur vient d'être créé pour vous sur la plateforme.
                    </p>
                    <h3 style="color: #2c2c2c; margin-bottom: 20px; text-align: center;">Voici vos informations de connexion :</h3>
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="display: inline-block; background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 4px; padding: 10px 20px; margin: 10px; width: 80%; font-size: 16px;">
                            <strong>Adresse e-mail :</strong> {email}
                        </div>
                        <div style="display: inline-block; background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 4px; padding: 10px 20px; margin: 10px; width: 80%; font-size: 16px;">
                            <strong>Mot de passe :</strong> {temp_password}
                        </div>
                    </div>
                    <p style="color: #2c2c2c; text-align: center; margin-bottom: 20px; font-style: italic;">
                        Pour raisons de sécurité, le mot de passe sera demandé de définir un nouveau mot de passe lors de votre première connexion.
                    </p>
                    <p style="color: #2c2c2c; text-align: center; margin-bottom: 20px;">
                        Vous pouvez vous connecter dès maintenant à votre tableau de bord :
                    </p>
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="{Dotenv.BACK_OFFICE_URL}" style="background-color: #007bff; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                            Accéder au tableau de bord
                        </a>
                    </div>
                    <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; padding: 20px; margin-top: 30px;">
                        <p style="color: #155724; margin: 0; font-weight: 600; text-align: center;">
                            ℹ️ <strong>Information importante :</strong>
                        </p>
                        <p style="color: #155724; margin-top: 10px; margin-bottom: 0; font-size: 14px; line-height: 1.6; text-align: center;">
                            Si vous n'êtes pas à l'origine de cette inscription, vous pouvez sans qu'il y ait de souci nous contacter.
                        </p>
                    </div>
                    <p style="color: #2c2c2c; text-align: center; margin-top: 30px; margin-bottom: 10px;">
                        Si vous rencontrez des difficultés à l'accès, ou si vous souhaitez qu'on vous aide, n'hésitez pas à contacter immédiatement notre équipe de support à <a href="mailto:support@flask.python">support@pflask.python</a>.
                    </p>
                    <p style="color: #2c2c2c; text-align: center; margin-bottom: 20px; font-style: italic;">
                        Merci de faire partie de cette aventure,
                    </p>
                    <p style="color: #2c2c2c; text-align: center; font-weight: bold; margin-bottom: 40px;">
                        L'équipe de Support
                    </p>
                </div>
            """
            
            if email_service.send_email(email, subject, message, None, "admin_welcome"):
                logger.info(f"Mail de bienvenue admin envoyé à {email}")
                return True
            else:
                logger.error(f"Échec de l'envoi du mail de bienvenue admin à {email}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du mail de bienvenue admin pour {email}: {str(e)}")
            raise e


    @staticmethod
    def send_account_activation_code(user: User) -> Optional[str]:
        try:
            account_activation_code = pyotp.TOTP(
                s=UserAdaptater.generate_account_activation_secret(user),
                digits=Config.OTP_DIGITS_NUMBER,
                interval=Config.OTP_EXPIRATION_TIMEOUT
            ).now()

            user_civility = "M. " if (user.gender == UserGender.MALE.value) else "Mme/Mlle " if (user.gender == UserGender.FEMALE.value) else ""
            user_name = f"{user_civility}{user.lastname} {user.firstname}"

            if email_service.send_welcome_email(user.email, user_name, account_activation_code):
                logger.info(f"Code d'activation envoyé à {user.email}")
            else:
                logger.error(f"Échec de l'envoi du code d'activation à {user.email}")
            
            return account_activation_code
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du code d'activation pour {user.email}: {str(e)}")
            raise e


    @staticmethod
    def resend_account_verification_code(email: str) -> Optional[str]:
        try:
            user = UserAdaptater.get_by_email(email)

            if not user:
                logger.warning(f"Tentative de renvoi de code de vérification pour un email inexistant: {email}")
                raise e

            account_activation_code = pyotp.TOTP(
                s=UserAdaptater.generate_account_activation_secret(user),
                digits=Config.OTP_DIGITS_NUMBER,
                interval=Config.OTP_EXPIRATION_TIMEOUT
            ).now()

            subject = "🔄 Renvoi de votre code de vérification"
            message = """
                <h2 style="color: #2c2c2c; margin-bottom: 20px;">Renvoi du code de vérification</h2>
                <p>Vous avez demandé le renvoi de votre code de vérification de compte.</p>
                <p>Voici votre nouveau code d'activation :</p>
                <p style="margin-top: 30px;"><strong>📱 Comment utiliser ce code :</strong></p>
                <ul style="margin-left: 20px; color: #2c2c2c;">
                    <li>Ouvrez l'application</li>
                    <li>Accédez à la section "Vérification du compte"</li>
                    <li>Saisissez le code ci-dessus</li>
                    <li>Votre compte sera activé immédiatement</li>
                </ul>
                <p style="margin-top: 30px; font-style: italic; color: #666;">
                    Ce code remplace tous les codes précédents et expire dans 5 minutes.
                </p>
            """
            
            if email_service.send_email(user.email, subject, message, account_activation_code, "account_verification_resend"):
                logger.info(f"Code de vérification renvoyé à {email}")
                return account_activation_code
            else:
                logger.error(f"Échec du renvoi du code de vérification à {email}")
                raise e
                
        except Exception as e:
            logger.error(f"Erreur lors du renvoi du code de vérification pour {email}: {str(e)}")
            raise e
