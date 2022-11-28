import smtplib
from email.mime.text import MIMEText
import win32com.client
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def lst_eachMailingList():

    import pandas as pd
    import xlwings as xw

    fileName = "../mailinglist.xlsx"
    sheetName = "sheet1"

    book = xw.Book(fileName)
    df = book.sheets(sheetName).used_range.options(pd.DataFrame).value

    mailingListAll = df['이메일'].tolist()
    n = 50
    lst_eachMailingList = [','.join(mailingListAll[i * n:(i + 1) * n]) for i in range((len(mailingListAll) - 1 + n) // n)]

    print(lst_eachMailingList)
    return lst_eachMailingList


# Mail 준비
smtp_server = '10.18.1.69'                 # 메일서버
mail_id = 'H147000M_HMAP'                  # ID
mail_passwd = 'A!0M_HMAP'                  # 비밀번호
mail_sender = 'hmaphelper@hdec.co.kr'      # 이메일

server = smtplib.SMTP(smtp_server)
server.ehlo()
server.starttls()
server.login(mail_id, mail_passwd)

bodyText = "테스트메일"
subject = "테스트메일입니다. "



to_user = []
to_user = lst_eachMailingList()
print(to_user)

for mTo_User in to_user :
    msg = MIMEText(bodyText, 'html', _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = mail_sender
    # msg["To"] = mTo_User  # 수신자
    # msg["Cc"]   # 참조
    msg["Bcc"] = mTo_User # 숨은참조

    try :
        server.send_message(msg)
    except :
        print ('error sending mail')
