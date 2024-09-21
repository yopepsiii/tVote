from mailersend import emails

from config import settings


class MailService:
    client = emails.NewEmail(settings.ms_api_key)

    @classmethod
    def send_email(cls, to: list, subject, text):
        mail_body = {}

        mail_from = {
            "name": "tVote",
            "email": f"noreply@{settings.ms_domain}",
        }

        recipients = to

        mail_client = cls.client

        mail_client.set_mail_from(mail_from, mail_body)
        mail_client.set_mail_to(recipients, mail_body)
        mail_client.set_subject(subject, mail_body)
        mail_client.set_plaintext_content(text, mail_body)

        res = mail_client.send(mail_body)

        print(f"INFO: \tПользователь {to[0]['name']} ({to[0]['email']}) --- {res}")

        # Заскоментировать для тестов, чтобы не тратить лимиты
        # return True
