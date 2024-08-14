import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from mimetypes import guess_type
from typing import List, Union

from var_env import VAR_ENV

class EmailUtils:
    @classmethod
    def send_email(
        cls,
        to: Union[List[str], str],
        subject: str,
        html_content: str,
        sender_name: str = "Leasing Total",
    ) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((sender_name, VAR_ENV['EMAIL']['SENDER']))

        to_list = to
        if type(to) == list:
            to = ",".join(to)

        msg["To"] = to

        part = MIMEText(html_content, "html")
        msg.attach(part)

        with smtplib.SMTP(VAR_ENV['EMAIL']['HOST'], VAR_ENV['EMAIL']['PORT']) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(VAR_ENV['EMAIL']['USERNAME_SMTP'], VAR_ENV['EMAIL']['PASSWORD_SMTP'])
            server.sendmail(VAR_ENV['EMAIL']['SENDER'], to_list, msg.as_string())
