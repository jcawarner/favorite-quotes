from tkinter import *
from PIL import ImageTk, Image
import requests
import json
import sqlite3
from gtts import gTTS
from pygame import mixer
import random

#set up Tkinter window
window = Tk()
window.title("Quotes")
window.geometry("550x500")


#quote api
url = "https://quotes15.p.rapidapi.com/quotes/random/"

headers = {
    'x-rapidapi-host': "quotes15.p.rapidapi.com",
    'x-rapidapi-key': "ef40eaf520msh733eda9215e1f99p16edb1jsn67d51e5b20f8"
    }

response = requests.request("GET", url, headers=headers)
quote = json.loads(response.content)

def save():
	global quote
	#set up database
	conn = sqlite3.connect('quotes.db')

	#create cursor
	c = conn.cursor()

	#create table
	# c.execute("CREATE TABLE Quotes (author text, quote text)")
	c.execute(f"INSERT INTO Quotes (author, quote) VALUES (?,?)", (quote['originator']['name'], quote['content']))


	#commit changes
	conn.commit()

	#close connection
	conn.close()

def next():
	response = requests.request("GET", url, headers=headers)
	global quote
	quote = json.loads(response.content)
	random_quote.config(text=quote['content'])
	author.config(text= "-" + quote['originator']['name'])


count = 0
def play():
	global quote
	global count
	mytext = quote['content']
	language = 'en'
	myobj = gTTS(text=mytext, lang=language, slow=True, tld='co.uk')
	myobj.save(f"quote{count}.mp3")
	mixer.init()
	mixer.music.load(f"quote{count}.mp3")
	mixer.music.play()
	count += 1

def favorite():
	global quote
	# set up database
	conn = sqlite3.connect('quotes.db')

	# create cursor
	c = conn.cursor()

	# create table
	# c.execute("CREATE TABLE Quotes (author text, quote text)")
	c.execute("SELECT * FROM Quotes")

	fav_quotes = c.fetchall()
	ran_quote = random.randint(0,len(fav_quotes)-1)
	random_quote.config(text=fav_quotes[ran_quote][1])
	author.config(text="-" + fav_quotes[ran_quote][0])

	# commit changes
	conn.commit()

	# close connection
	conn.close()


path = "canvas_med.jpg"
width = 700
height = 800
# background_img = ImageTk.PhotoImage(Image.open(path))
background_img = Image.open(path)
background_img = background_img.resize((width,height))
photo_bg = ImageTk.PhotoImage(background_img)
save_img = PhotoImage(file="save2.png")
next_img = PhotoImage(file="next.png")
play_img = PhotoImage(file="play.png")
fav_img = PhotoImage(file="favorite_1.png")


canvas = Canvas(width=1100, height=1000, highlightthickness=0)
canvas.create_image(200,100, image=photo_bg)
canvas.grid(row=0, column=0)


random_quote = Message(window, text=quote['content'])
random_quote.config(fg="white", bg="#b49368", font=("Arial", 20, 'italic'), width=500)
random_quote.place(x=25, y=25)

author = Label(window, text= "-" + quote['originator']['name'], fg='white', bg = "#96704b", font=("Arial", 20, 'italic'))
author.place(x=150, y=375)


# next
next_button = Button(window, image= next_img, highlightthicknes=0, bd=0, bg="#96704b", activebackground= "#96704b", command=next)
next_button.place(x=350, y=440)

save_button = Button(window, image= save_img, highlightthickness=0, bd=0, bg="#96704b", activebackground = "#96704b", command=save)
save_button.place(x=50, y=440)

play_button = Button(window, image = play_img, bg="#96704b", highlightthickness=0, bd=0, activebackground= '#96704b', command=play)
play_button.place(x=260, y=440)

fav_button = Button(window, image = fav_img, bg="#96704b", highlightthickness=0, bd=0, activebackground= '#96704b', command=favorite)
fav_button.place(x=180, y=440)


window.mainloop()