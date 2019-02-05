import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']

@ask.launch
def launch():
    speech_text = 'Welcome to your smart home.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)
#lights
@ask.intent('Lights', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(16,GPIO.OUT)
    if status in STATUSON:
	GPIO.output(16,GPIO.HIGH)
	return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        GPIO.output(16,GPIO.LOW)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')
#outlet 
@ask.intent('Outlet', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(18,GPIO.OUT)
    if status in STATUSON:
	GPIO.output(18,GPIO.HIGH)
	return statement('turning {} the outlet'.format(status))
    elif status in STATUSOFF:
        GPIO.output(18,GPIO.LOW)
        return statement('turning {} the outlet'.format(status))
    else:
        return statement('Sorry not possible.')
#router
 @ask.intent('Router', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(22,GPIO.OUT)
    if status in STATUSON:
	GPIO.output(22,GPIO.HIGH)
	return statement('turning {} the router'.format(status))
    elif status in STATUSOFF:
        GPIO.output(22,GPIO.LOW)
        return statement('turning {} the router'.format(status))
    else:
        return statement('Sorry not possible.')
#purge
#Turns off all the lights and commands this is for testing purposes only
@ask.intent('Purge')
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
	GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)

#test
#Turns on all the lights and commands this is for testing purposes only
@ask.intent('Purge')
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
	GPIO.output(16,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(22,GPIO.HIGH)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You canYou can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
app.run(debug=True)