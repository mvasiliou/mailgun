import requests

class Mailgun:

    def __init__(self, api_key, domain_name):
        self.api_key = api_key
        self.domain_name = domain_name

    def send_simple_message(self, subject, message, recipients, sender_name, sender_email):
        self.send_message(subject, message, recipients, sender_name, sender_email)

    def send__message(self, subject, message, recipients, sender_name, sender_email, attachments = [], cc = None, bcc = None, deliverytime = None, campaign = None, tag = None, dkim = False, testmode = False, tracking = True, tracking_opens = True, tracking_clicks = True, require_tls = False, skip_verification = False):
        
        if type(attachments) is str:
            attachments = [attachments]

        files = []
        for file in attachments:
            files.append(("attachment", open(file)))

        if type(recipients) is str:
            recipients = [recipients]

        return requests.post(
            "https://api.mailgun.net/v3/"+self.domain_name+"/messages",
            auth=("api", self.api_key),
            files=files,
            data={"from": sender_name + " <" + sender_email + ">",
                  "to": recipients,
                  "cc": cc,
                  "bcc": bcc,
                  "subject": subject,
                  "html": message,
                  "o:campaign": campaign,
                  "o:tag": tag,
                  "o:dkim": dkim,
                  "o:deliverytime": deliverytime,
                  "o:testmode": testmode,
                  "o:tracking": tracking,
                  "o:tracking-opens": tracking_opens,
                  "o:tracking-clicks": tracking_clicks,
                  "o:require-tls": require_tls,
                  "o:skip_verification": skip_verification})

    def create_user(self, sender_email, sender_name):
        api = self
        user = User(sender_email, sender_name, api)
        return user

class User:
    def __init__(self, sender_email, sender_name, api):
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.api = api

    def send_from_user(self, subject, message, recipients, files = []):
        self.api.send_message(subject, message, recipients, self.sender_name, self.sender_email, files = [])

# o:deliverytime  Desired time of delivery. See Date Format. Note: Messages can be scheduled for a maximum of 3 days in the future.

# inline  Attachment with inline disposition. Can be used to send inline images (see example). You can post multiple inline values.

# h:X-My-Header   h: prefix followed by an arbitrary value allows to append a custom MIME header to the message (X-My-Header in this case). For example, h:Reply-To to specify Reply-To address.
# v:my-var    v: prefix followed by an arbitrary name allows to attach a custom JSON data to the message. See Attaching Data to Messages for more information.

if __name__ == "__main__":
    api = Mailgun("key-857c49fcaa269d0d13d9bed33630f786","mikevasiliou.com")
    api.send__message("Test Subject","Test Message", "mvasiliou94@gmail.com","Mike V", "warroom@mikevasiliou.com")
