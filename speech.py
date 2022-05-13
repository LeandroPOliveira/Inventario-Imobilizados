from datetime import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='pt-BR')
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)

    except:
        print('não entendi')
    return command

def run_alexa():
    comando = take_command()
    print(comando)
    if 'tocar' in comando:
        musica = comando.replace('tocar', '')
        talk('tocando' + musica)
        pywhatkit.playonyt(musica)
    elif 'hora' in comando:
        hora = datetime.now().strftime('%I:%M')
        print(hora)
        talk('Agora são' + hora)


while True:
    run_alexa()



