import imaplib
import email
import traceback


MY_EMAIL = "mac00990011@gmail.com"
# For the password to work use app password to create a specific password
# to be used for the program. Like the password below created for this specific
# program. Can be deleted after use.
password = "*************"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 993  # Standard IMAP SSL port

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

        for i in range(latest_email_id, latest_email_id-10, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1], 'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
        # Close the connection
        mail.logout()

    except Exception as e:
        traceback.print_exc()
        print(str(e))


read_email()