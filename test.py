import imaplib
import email
import json
import traceback
import string

dictionary = {}
with open('password.json', 'r') as file:
    data = json.load(file)
MY_EMAIL = data['username']
password = data['password']
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 993  # Standard IMAP SSL port


def store_email(frm, subject, count):
    frm = frm.split("<")
    frm = frm[0]
    if '0' not in dictionary:
        dictionary.setdefault(count, {}).setdefault('From', f"{frm}")
        dictionary.setdefault(count, {}).setdefault('Subject', f"{subject}")
    else:
        dictionary.setdefault(count, {}).setdefault('From', f"{frm}")
        dictionary.setdefault(count, {}).setdefault('Subject', f"{subject}")
    with open('dictionary', 'w') as dictfile:
        json.dump(dictionary, dictfile, indent=4)

def read_email():
    try:
        # Initialize the IMAP connection
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        # Log in to your account
        mail.login(MY_EMAIL, password)
        # Select a mailbox (e.g., INBOX)
        mail.select('inbox')

        # Fetch emails, etc.
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        latest_email_id = int(id_list[-1])
        count = 0
        for i in range(latest_email_id, latest_email_id - 10, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    store_email(email_from, email_subject, count)
                    count = count + 1
        # Close the connection
        mail.logout()

    except Exception as e:
        traceback.print_exc()
        print(str(e))


read_email()