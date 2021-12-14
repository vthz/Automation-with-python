import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()

content = ""


def extract_news(url):
    print("Extracting news, please wait...")
    temp = " "
    temp += ("<b>HN Top News Stories:</b>\n" + "<br>" + "-" * 50 + "<br>")
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    for i, tag in enumerate(soup.find_all("td", attrs={"class": "title", "valign": ""})):
        temp += (str(i + 1) + " :: " + tag.text + "\n" + "<br>") if tag.text != "More" else " "
    return temp


temp = extract_news("https://news.ycombinator.com/")
content += temp
content += "<br>-----This is computer generated email!-----<br>"
content += "<br><br>End of Message"

print("Composing Email...")
SERVER = "smtp.gmail.com"
PORT = 587
FROM = "***"
TO = "***"
PASS = "***"

msg = MIMEMultipart()
msg["Subject"] = "Top News Stories HN [Automated email]" + " " + str(now.day) + "-" + str(now.month) + "-" + str(
    now.year)
msg["From"] = FROM
msg["To"] = TO
msg.attach(MIMEText(content, "html"))

print("Initiating server...")
server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())
print("Email sent!")
server.quit()
