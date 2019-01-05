import smtplib



#server connection with gmail only
global server
server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
# error catcher we can set the level of error checking currenly 0 can be 
server.set_debuglevel(0)
#chose who is receiver and who is sender
toemail=""
fromemail="jamesfingerless@gmail.com"
#sender's password
password="hacker228"

#message subject and content
message_subject = "Text message test"
message_text = "Today is a very good day"
message = "From: %s\r\n" % fromemail + "To: %s\r\n" % toemail + "Subject: %s\r\n" % message_subject+ "\r\n" + message_text
#login to server
server.login(fromemail,password)


#sends the mail
#send(fromemail,toemail,message)

     




