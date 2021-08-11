
# SENDER

import argparse
import sys
import time
from keygen import gen

from chirpsdk import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE

from tkinter import *


divMsg = []



def encode(s):
    return bytearray([ord(ch) for ch in s])



class Callbacks(CallbackSet):
    end = encode("@6a!9$Sx")

    current = ""


    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        print('State changed from {} to {}'.format(
            CHIRP_CONNECT_STATE.get(previous_state),
            CHIRP_CONNECT_STATE.get(current_state)))

    def on_sending(self, payload, channel):
        """ Called when a chirp has started to be transmitted """
        print('Sending: {data} [ch{ch}]'.format(
            data=list(payload), ch=channel))

    def on_sent(self, payload, channel):
        """ Called when the entire chirp has been sent """
        print('Sent: {data} [ch{ch}]'.format(
            data=list(payload), ch=channel))

    def on_receiving(self, channel):
        """ Called when a chirp frontdoor is detected """
        print('Receiving data [ch{ch}]'.format(ch=channel))

    def on_received(self, payload, channel):
        """
        Called when an entire chirp has been received.
        Note: A payload of None indicates a failed decode.
        """
        if payload is None:
            print('Decode failed!')
        else:
            if payload != self.end:
                chunk = payload.decode("utf-8")
                self.current += chunk
                print("Chunk: " + chunk)
                # print('Received: {data} [ch{ch}]'.format(data=chunk, ch=channel))
            else:
                print("Message: " + self.current)
                self.current = ""



def divideMsg8(msg):
    for x in range(int(len(msg) / 8) + 1):
        divMsg.append(msg[0:8])
        msg = msg[8:]
    if len(divMsg[-1]) < 5:
        divMsg[-1] += " " * (5 - len(divMsg[-1]))
        #print(msg)




def main(block_name, input_device, output_device, block_size, sample_rate, string):

    # Initialise ConnectSDK
    sdk = ChirpConnect(block=block_name)
    print(str(sdk))
    print('Protocol: {protocol} [v{version}]'.format(
        protocol=sdk.protocol_name,
        version=sdk.protocol_version))
    print(sdk.audio.query_devices())

    # Configure audio
    sdk.audio.input_device = input_device
    sdk.audio.output_device = output_device
    sdk.audio.block_size = block_size
    sdk.input_sample_rate = sample_rate
    sdk.output_sample_rate = 44100

    # Set callback functions
    sdk.set_callbacks(Callbacks())

    # print("type your message")
    #msg = ""
    print(string)
    divideMsg8(string)
    #print(divMsg)

    # window = Tk()

    # messages = Text(window)
    # messages.pack()

    # # input_user = StringVar()
    # # input_field = Entry(window, text=input_user)
    # input_field.pack(side=BOTTOM, fill=X)

    # def Enter_pressed(event):
    #     input_get = input_field.get()
    #     global msg, divMsg
    #     msg = input_get
    #     divMsg = divideMsg8(string)
    #     #print(input_get)
    #     messages.insert(INSERT, '%s\n' % input_get)

    #     # label = Label(window, text=input_get)
    #     input_user.set('')
    #     # label.pack()
    #     return "break"

    # frame = Frame(window)  # , width=300, height=300)
    # input_field.bind("<Return>", Enter_pressed)
    # frame.pack()

    # window.mainloop()

    #initialize SDK to SEND ONLY
   
    
    sdk.start(send=True, receive=True)

    timeLapse = 0;
    # numMsgSent = 0;

    try:
        # Process audio streams
        while True:
            
            if string != "xS$9!a6@":

                time.sleep(0.1)
                # sys.stdout.write('.')
                sys.stdout.flush()
                timeLapse += 1
                if timeLapse % 50 == 0:
                    timeLapse = 0
                    # if numMsgSent <= len(divMsg):
                    if len(divMsg) > 0:
                        # identifier = divMsg[numMsgSent]
                        identifier = divMsg[0]
                        payload = bytearray([ord(ch) for ch in identifier])
                        sdk.send(payload)
                        divMsg.pop(0)
                        # numMsgSent += 1
                    else:
                        identifier = "@6a!9$Sx"
                        payload = bytearray([ord(ch) for ch in identifier])
                        sdk.send(payload)
                        time.sleep(5)
                        break
            else:
                time.sleep(0.1)
                 # sys.stdout.write('.')
                sys.stdout.flush()
                break


    except KeyboardInterrupt:
        print('Exiting')

    sdk.stop()


if __name__ == '__main__':
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

    main(args.c, args.i, args.o, args.b, args.s)