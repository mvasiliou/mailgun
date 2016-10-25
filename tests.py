import mailgun

def get_token(file_name):
    infile = open(file_name, 'r')
    token = infile.readline()
    infile.close()
    return token

if __name__ == "__main__":
    api_key = get_token("mailgun_key.txt")
    domain = get_token("domain.txt")
    receiver = get_token("receiver.txt")
    sender = get_token("sender.txt")
    api = mailgun.Mailgun(api_key,domain)
    api.send__message("Test Subject","Test Message", receiver, "Mailgun Python Wrapper", sender)
    logs = api.get_logs()
    print(logs.text)