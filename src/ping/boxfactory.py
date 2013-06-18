
import ping.popbox
import ping.imapbox

def get_inbox(account):
    '''
    gets the correct inbox type when called.
    '''
    if account.type == 'POP':
        inbox = ping.popbox.PopBox(account)
    if account.type == 'IMAP':
        inbox = ping.imapbox.ImapBox(account)
    return inbox