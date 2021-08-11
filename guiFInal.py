import argparse
import sys
import time
from keygen import gen

from chirpsdk import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE
from sender import *
from tkinter import *
root = Tk()


root.config(bg = "blue")
w = 500
h = 500
root.geometry("500x500")
label1 = Label( root, text="Write a message")
label1.config(bg = "blue", fg = "white")
E1 = Entry(root, bd =5)
E1.config(width= 100)
def sendmessage():
	# print(E1.get())

	parser = argparse.ArgumentParser(
		description='ChirpSDK Demo',
		epilog='Sends a random chirp payload, then continuously listens for chirps'
	)   
	parser.add_argument('-c', help='The configuration block [name] in your ~/.chirprc file (optional)')
	parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
	parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
	parser.add_argument('-b', type=int, default=0, help='Block size (optional)')
	parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
	args = parser.parse_args()

	main(args.c, args.i, args.o, args.b, args.s, E1.get())


submit = Button(root, text ="Submit",fg = "red", command = sendmessage)
submit["background"] = "yellow"
# submit.config(fg = "yellow")
submit.grid(row=int(w/2 +1000), column=int (h/2 +500))
label1.pack()
E1.pack()
submit.pack() 

root.mainloop()
# while (i==0):
# 	parser = argparse.ArgumentParser(
# 		description='ChirpSDK Demo',
# 		epilog='Sends a random chirp payload, then continuously listens for chirps'
# 	)   
# 	parser.add_argument('-c', help='The configuration block [name] in your ~/.chirprc file (optional)')
# 	parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
# 	parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
# 	parser.add_argument('-b', type=int, default=0, help='Block size (optional)')
# 	parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
# 	args = parser.parse_args()

# 	main(args.c, args.i, args.o, args.b, args.s, "xS$9!a6@")
