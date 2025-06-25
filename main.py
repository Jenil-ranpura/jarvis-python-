import speech_recognition as sr
import pyttsx3
import musicLibrary
import openai

recog = sr.Recognizer()
engine = pyttsx3.init()
mic = sr.Microphone()

openai.api_key = "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"

def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful and intelligent assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error contacting AI service: {e}"

def speak(text):
    print(f"The Text Is : {text}")
    engine.say(text)
    engine.runAndWait()
    
def processcommand(c):
    if "open youtube" in c.lower():
        import webbrowser
        webbrowser.open("https://www.youtube.com/")
    
    elif "open google" in c.lower():
        import webbrowser
        webbrowser.open("https://www.google.com/")
        
    elif "open facebook" in c.lower():
        import webbrowser
        webbrowser.open("https://www.facebook.com/")
        
    elif "play shikari" in c.lower():
        import webbrowser
        webbrowser.open(musicLibrary.music["shikari"])
        
    elif "play nopole" in c.lower():
        import webbrowser
        webbrowser.open(musicLibrary.music["nopole"])
        
    elif "play peligrosa" in c.lower():
        import webbrowser
        webbrowser.open(musicLibrary.music["peligrosa"])
        
    else:
        # have the answers from open ai
        speak("Let me think...")
        gpt_reply = ask_gpt(c)
        speak(gpt_reply)
            

def talkToMe():
    mic_stream = mic.__enter__()
    print("Listening...")
    
    try:
        audio = recog.listen(mic_stream, timeout=2)
        print("Recognizing...")
        text = recog.recognize_google(audio)
        
        if "exit" in text.lower():
            print("Exiting by voice command...")
            engine.say("Goodbye!")
            engine.runAndWait()
            exit()
            return
        
        elif text.lower() == "jarvis":
            print("Jarvis Activatd...")
            engine.say("Yes Boss")
            engine.runAndWait()            

            audio = recog.listen(mic_stream, timeout=2)
            print("Recognizing...")
            text = recog.recognize_google(audio)
            
            processcommand(text)

        speak(text)
        
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand what you said.")
        
    except sr.RequestError:
        speak("Network error or Google service is down.")
        
    except Exception as e:
        speak(f"An unexpected error occurred: {e}")
        
    finally:
        mic.__exit__(None, None, None)
        
while True:
    talkToMe()


