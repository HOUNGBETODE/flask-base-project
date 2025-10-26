from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from commons.helpers.load_doten import Dotenv
from commons.instances.instances import logger


class EmailService:

    def __init__(self):
        # Charger les informations SMTP à partir de l'environnement
        self.smtp_server = Dotenv.SMTPSERVEUR
        self.smtp_port = Dotenv.SMTPPORT
        self.smtp_user = Dotenv.SMTPUSER
        self.smtp_password = Dotenv.SMTPPASSWORD
        self.logo_path = os.path.join(os.path.dirname(__file__), '../../static/images/logo/logo.png')

    def _get_email_template(self, message: str, verification_code: str = None, email_type: str = "default") -> str:
        # Section de code de vérification si nécessaire
        verification_section = ""
        if verification_code:
            verification_section = f"""
                <div class="verification-code">
                    <div class="code-label">Votre code de vérification :</div>
                    <div class="code-value">{verification_code}</div>
                    <div class="code-info">Ce code est valide pendant 10 minutes.</div>
                </div>
                <div class="cta-text">
                    Veuillez saisir sur la page de vérification afin de confirmer que vous êtes bien le propriétaire légitime de ce compte.
                </div>
                <div class="warning">
                    À ignorer cette connexion si vous n’êtes pas à l’origine de celle-ci. Votre compte reste protégé.
                </div>
            """

        # Message personnalisé basé sur le type pour s'aligner sur le format de l'image
        if email_type == "welcome":
            intro_message = f"""
                <div class="greeting">Bonjour {message.split('!')[0].replace('Bonjour ', '')},</div>
                <div class="title">Voici votre code de vérification</div>
                <div class="intro-text">
                    Pour garantir la sécurité de votre compte, nous devons vérifier votre identité. 
                    Utilisez le code ci-dessous pour vérifier votre connexion.
                </div>
            """
        elif email_type == "password_reset":
            intro_message = """
                <div class="greeting">Bonjour,</div>
                <div class="title">Voici votre code de vérification</div>
                <div class="intro-text">
                    Pour réinitialiser votre mot de passe, nous devons vérifier votre identité. 
                    Utilisez le code ci-dessous pour procéder à la réinitialisation.
                </div>
            """
        else:
            intro_message = message  # Pour les types par défaut, utiliser le message fourni

        return f"""
        <!DOCTYPE html>
        <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Flask - Email</title>
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.5;
                        color: #333;
                        background-color: #f5f5f5;
                        padding: 20px 0;
                    }}
                    
                    .email-container {{
                        max-width: 500px;
                        margin: 0 auto;
                        background: #ffffff;
                        border-radius: 12px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    
                    .logo {{
                        text-align: center;
                        padding: 30px 20px 20px;
                    }}
                    
                    .logo img {{
                        width: 60px;
                        height: auto;
                    }}
                    
                    .content {{
                        padding: 0 30px 30px;
                    }}
                    
                    .greeting {{
                        font-size: 18px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: #333;
                    }}
                    
                    .title {{
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 15px;
                        color: #333;
                    }}
                    
                    .intro-text {{
                        font-size: 14px;
                        margin-bottom: 25px;
                        color: #666;
                    }}
                    
                    .verification-code {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    
                    .code-label {{
                        font-weight: bold;
                        margin-bottom: 15px;
                        font-size: 16px;
                        color: #333;
                    }}
                    
                    .code-value {{
                        border: 2px solid #ddd;
                        border-radius: 8px;
                        padding: 20px;
                        font-size: 32px;
                        font-family: 'Courier New', monospace;
                        letter-spacing: 8px;
                        background: #f9f9f9;
                        margin: 0 auto 15px;
                        width: 200px;
                        text-align: center;
                        color: #333;
                        font-weight: bold;
                    }}
                    
                    .code-info {{
                        font-size: 14px;
                        color: #999;
                        margin-bottom: 20px;
                    }}
                    
                    .cta-text {{
                        font-size: 14px;
                        color: #666;
                        text-align: center;
                        margin: 20px 0;
                        line-height: 1.4;
                    }}
                    
                    .warning {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 20px 0;
                        font-size: 14px;
                        color: #856404;
                        line-height: 1.4;
                    }}
                    
                    .footer {{
                        text-align: center;
                        padding: 25px 30px;
                        border-top: 1px solid #eee;
                        font-size: 12px;
                        color: #999;
                        position: relative;
                    }}
                    
                    .footer-title {{
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: #333;
                    }}
                    
                    .footer-copyright {{
                        position: absolute;
                        left: 30px;
                        bottom: 25px;
                        text-align: left;
                        color: #999;
                    }}
                    
                    .footer-social {{
                        position: absolute;
                        right: 30px;
                        bottom: 25px;
                        text-align: right;
                        color: #999;
                    }}
                    
                    .footer-social a {{
                        color: #999;
                        text-decoration: none;
                        margin: 0 5px;
                    }}
                    
                    @media (max-width: 500px) {{
                        .email-container {{
                            margin: 10px;
                            border-radius: 8px;
                        }}
                        
                        .content {{
                            padding: 0 20px 20px;
                        }}
                        
                        .logo {{
                            padding: 20px 20px 15px;
                        }}
                        
                        .code-value {{
                            font-size: 24px;
                            letter-spacing: 4px;
                            width: 150px;
                            padding: 15px;
                        }}
                        
                        .footer-copyright,
                        .footer-social {{
                            position: static;
                            text-align: center;
                            margin: 5px 0;
                        }}
                        
                        .footer-social {{
                            margin-top: 5px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="logo">
                        <img src="cid:logo" alt="Flask Logo">
                    </div>
                    
                    <div class="content">
                        {intro_message}
                        
                        {verification_section}
                    </div>
                    
                    <div class="footer">
                        <div class="footer-copyright">@2025 Flask</div>
                        <div class="footer-social">
                            Facebook • <a href="#">Instagram</a> • <a href="#">TikTok</a>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """

    def send_email(self, to_email: str, subject: str, message: str, verification_code: str = None, email_type: str = "default") -> bool:
        try:
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = f"Flask Platform <{self.smtp_user}>"
            msg['To'] = to_email
            
            # Headers additionnels pour améliorer la délivrabilité
            msg['Reply-To'] = self.smtp_user
            msg['X-Mailer'] = 'Flask Mailer'

            # Génération du contenu HTML
            html_content = self._get_email_template(message, verification_code, email_type)
            
            # Attacher le contenu HTML
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Attacher le logo si il existe
            if os.path.exists(self.logo_path):
                with open(self.logo_path, 'rb') as img:
                    logo = MIMEImage(img.read())
                    logo.add_header('Content-ID', '<logo>')
                    logo.add_header('Content-Disposition', 'inline', filename='flask_logo.png')
                    msg.attach(logo)
            else:
                logger.warning(f"Logo non trouvé à l'emplacement: {self.logo_path}")

            # Envoyer l'email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, to_email, msg.as_string())
            
            logger.info(f"Email envoyé avec succès à {to_email} - Sujet: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {to_email}: {str(e)}")
            return False


    def send_welcome_email(self, to_email: str, user_name: str, verification_code: str) -> bool:
        subject = "🎉 Bienvenue sur cette plateforme !"
        # Le message est maintenant géré dans le template via email_type="welcome"
        # user_name est extrait pour le greeting dans le template
        return self.send_email(to_email, subject, user_name, verification_code, "welcome")


    def send_password_reset_email(self, to_email: str, verification_code: str) -> bool:
        subject = "🔐 Réinitialisation de votre mot de passe"
        # Le message est maintenant géré dans le template via email_type="password_reset"
        return self.send_email(to_email, subject, "", verification_code, "password_reset")
