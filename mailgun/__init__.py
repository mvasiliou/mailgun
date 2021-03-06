import requests

class Mailgun:

    def __init__(self, api_key, domain_name):
        self.api_key = api_key
        self.domain_name = domain_name

    def send_simple_message(self, subject, message, recipients, sender_name, sender_email):
        return self.send_message(subject, message, recipients, sender_name, sender_email)

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
            data={"from"              : sender_name + " <" + sender_email + ">",
                  "to"                : recipients,
                  "cc"                : cc,
                  "bcc"               : bcc,
                  "subject"           : subject,
                  "html"              : message,
                  "o:campaign"        : campaign,
                  "o:tag"             : tag,
                  "o:dkim"            : dkim,
                  "o:deliverytime"    : deliverytime,
                  "o:testmode"        : testmode,
                  "o:tracking"        : tracking,
                  "o:tracking-opens"  : tracking_opens,
                  "o:tracking-clicks" : tracking_clicks,
                  "o:require-tls"     : require_tls,
                  "o:skip_verification": skip_verification})

    def create_user(self, sender_email, sender_name):
        api = self
        user = User(sender_email, sender_name, api)
        return user

    def get_logs(self, begin = None, end = None, ascending = False, limit = 25, pretty = True, recipient = None, event = None, mailing_list = None, attachment = None, from_email = None, message_id = None, subject = None, to = None, size = None, tags = None, severity = None):
        return requests.get(
            "https://api.mailgun.net/v3/"+self.domain_name+"/events",
            auth=("api", self.api_key),
            params={"begin"       : begin,#"Fri, 3 May 2013 09:00:00 -0000",
                    "end"         : end,
                    "ascending"   : ascending,
                    "limit"       : limit,
                    "pretty"      : pretty,
                    "recipient"   : recipient,
                    "event"       : event,
                    "list"        : mailing_list,
                    "attachment"  : attachment,
                    "from"        : from_email,
                    "message-id"  : message_id,
                    "subject"     : subject,
                    "to"          : to,
                    "size"        : size,
                    "tags"        : tags,
                    "severity"    : severity})

    # AND 
    # OR
    # ""
    # NOT
    # > num
    # > num < num2

class User:
    def __init__(self, sender_email, sender_name, api):
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.api = api

    def send_from_user(self, subject, message, recipients, files = []):
        self.api.send_message(subject, message, recipients, self.sender_name, self.sender_email, files = [])


# inline  Attachment with inline disposition. Can be used to send inline images (see example). You can post multiple inline values.

# h:X-My-Header   h: prefix followed by an arbitrary value allows to append a custom MIME header to the message (X-My-Header in this case). For example, h:Reply-To to specify Reply-To address.
# v:my-var    v: prefix followed by an arbitrary name allows to attach a custom JSON data to the message. See Attaching Data to Messages for more information.


