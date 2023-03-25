import os
import speech_recognition as sr
import pyttsx3
import openai

def wait_for_trigger_word(recognizer, microphone, trigger_word):
    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            speech = recognizer.recognize_google(audio, show_all=True)

            if 'alternative' in speech:
                for alternative in speech['alternative']:
                    if trigger_word.lower() in alternative['transcript'].lower():
                        print("Trigger word detected!")
                        return
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))

def capture_command(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Please speak your command.")
        audio_command = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio_command)
        print("Command: " + command)
        return command
    except sr.UnknownValueError:
        print("Could not understand the command.")
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))

def handle_command(command, api_key):
    if command:
        # Set up the OpenAI API client
        openai.api_key = api_key

        # Send the command to ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{command}",
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Speak the response
        if response.choices:
            reply = response.choices[0].text.strip()
            print("Response:", reply)
            speak(reply)
        else:
            print("No response received.")
            speak("I'm sorry, I couldn't generate a response.")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main(api_key):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    trigger_word = "hey computer"

    print("Listening for the trigger word...")

    while True:
        wait_for_trigger_word(recognizer, microphone, trigger_word)
        speak("What is your command?")
        command = capture_command(recognizer, microphone)
        handle_command(command, api_key)

if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        main(api_key)
    else:
        print("Error: OPENAI_API_KEY environment variable not found.")
