from gtts import gTTS
from playsound import  playsound

mytext="Hello Geek! How are you doing??"
language='en'
myobj=gTTS(text=mytext,lang=language,slow=True)
myobj.save("welcome1.mp3")
playsound("welcome1.mp3")