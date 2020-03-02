import random
import time
import os

import speech_recognition as sr

##Musica
music_folder = "/var/shared/music/"
ostfolder = music_folder + "OST/"
playlistfolder = music_folder + "playlists/"
ratirl = playlistfolder + "ratirl_test_1/"
GG_ingame = playlistfolder + "GG_ingame/"
Deffolder = music_folder + "Def\ Con\ Dos/"
##GG
ggfolder = music_folder + "GuiltyGear/"
gg2 = ggfolder + "GuiltyGearRev2/"
ggsign = ggfolder + "GuiltyGearXrdSign"
#KPOP
kpopfolder = music_folder + "kpop/"
twicefolder = kpopfolder + "twice/"
bpinkfolder = kpopfolder + "blackpink/"
#OST folder
evafolder = ostfolder + "Evangelion\ OST/"
evaost2 = evafolder + "96-NGE-OST2/"
corpseparty = ostfolder + "Corpse\ Party\ OST/"
cpbos = corpseparty + "Corpse\ Party\ Book\ of\ Shadows\ OST/"
fatefolder = ostfolder + "Fate\ series\ OST/"
sinners = ostfolder + "The\ Garden\ of\ Sinners\ OST/Kara\ no\ Kyoukai\ Mirai\ Fukuin\ Original\ Soundtrack/"
Halo = ostfolder + "Halo\ OST/"
higurashi = ostfolder + 'Higurashi\ no\ naku\ koro\ OST/'
another = ostfolder + 'Another\ OST/'


#software = {"google chrome": "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Google Chrome.lnk"} #It Was A Test

playerdir=None
commandDictionary = {'guilty gear': ("music","playerdir=ggsign"),
                     'guilty gear rev 2': ("music","playerdir=gg2"),
                     'evangelion': ("music","playerdir=evafolder"),
                     'fate': ("music","playerdir=fatefolder"),
                     'corpse party': ("music","playerdir=corpseparty"),
                     'halo': ("music","playerdir=Halo"),
                     'higurashi': ("music","playerdir=higurashi"),
                     'another': ("music","playerdir=another"),
                     
                     
                     'stop': ("stop"),
                     'go kill yourself': ("""print("your mom is a whore, and i fucked her last night")""",
                                          "runBot=False")
                     }
missSpellingDictionary = {'faith':'fate'}

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        print('adjusting...')
        recognizer.adjust_for_ambient_noise(source)
        print('adjusted...')
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response


if __name__ == "__main__":
    # # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    time.sleep(0.5)
    print('Started...')
    runBot = True
    while runBot:
        recognize = True
        while recognize:
            conversion = recognize_speech_from_mic(recognizer, microphone)
            if conversion["transcription"]: recognize = False
            else: print("-- try again---")
        print('-- recognized')

        # if there was an error, stop the game
        if conversion["error"]:
            print("ERROR: {}".format(conversion["error"]))

        if runBot: 
            conversionLowCase = conversion["transcription"].lower()
            try:
                print(">> {}".format(conversion["transcription"]))
                try:
                    conversionLowCase = missSpellingDictionary[conversionLowCase]
                    print('[input update] >> {}'.format(conversionLowCase))
                except KeyError:
                    pass
                extraction = commandDictionary[conversionLowCase]
                if extraction[0] == 'music':
                    exec(extraction[1])
                    print(playerdir)
                    os.system("killall mpg123; find "+playerdir+"  -name '*.mp3' | sort --random-sort| head -n 100| xargs -d '\n' mpg123 -Z &")
                elif extraction[0] == 'stop': os.system("killall mpg123")
                else: pass

            except KeyError:
                print("[ERROR] Couldn't find an action for :{}".format(conversion["transcription"]))

print('cya')
