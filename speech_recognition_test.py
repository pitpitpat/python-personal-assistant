#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

activate_this = os.path.join(BASE_DIR, 'env/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """
    Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    with microphone as source:
        # print 'Adjusting for noise...'
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print 'Listening...'
        try:
            audio = recognizer.listen(source, timeout=0.3, phrase_time_limit=1)
        except sr.WaitTimeoutError:
            # speech was unintelligible
            response["error"] = "No speech detected"
            return response

    try:
        print 'Proccessing'
        response["transcription"] = recognizer.recognize_sphinx(audio)
        if response["transcription"] == 'Mila':
            import pyttsx
            import os
            text = 'Yes Sir!'
            os.system('say -v Karen "{}"'.format(text))
            with microphone as source:
                print 'Yes Sir!'
                audio = recognizer.listen(source, phrase_time_limit=3)
            print 'Proccessing'
            response["transcription"] = recognizer.recognize_google(audio, language='el-GR')
            engine = pyttsx.init()
            voice_id = 'com.apple.speech.synthesis.voice.melina'
            engine.setProperty('voice', voice_id)
            engine.say(response["transcription"])
            engine.runAndWait()
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def main():
    prompt_limit = 1000000

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    time.sleep(3)

    for j in range(prompt_limit):
        print 'Starting...'
        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"] or not guess["success"]:
            print("You said: {}\n".format(guess["transcription"].encode('utf8')))
        else:
            print("I didn't catch that. What did you say?\n")


if __name__ == "__main__":
    main()
