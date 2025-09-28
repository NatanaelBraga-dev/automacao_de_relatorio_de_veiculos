import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from variaveisDeAmbiente import username, password, baseDeVeiculos, dadosColhidosPeloBot

#CONEXÃO COM SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 
USERNAME = username
PASSWORD = password

sender_email = username #email do remetente
receiver_emails = ["emailquedesejareceberamensagem@gmail.com"] #coloque o email que deseja receber o arquivo
subject = "relatorio de veiculos"
body = "teste"

file_name = "dadosColhidosPeloBot.xlsx"
file_path = dadosColhidosPeloBot

#MONTANDO A MENSAGEM PARA ENVIO
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", " .join(receiver_emails)
message['Subject'] = subject

message.attach(MIMEText(body, "plain"))

#ADICIONANDO O ARQUIVO PARA ENVIO
with open(file_path, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={file_name}")
message.attach(part)

#ENVIANDO O EMAIL
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(sender_email, receiver_emails, message.as_string())

print("Email with attachment sent successfully!")