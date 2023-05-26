# Group Number: G14
# Members: Bob Bao, Tony Li, Sandy Chu, Glen Qiao
# webServer of the website
from flask import Flask, render_template, request, redirect
import socket

# setting of socket webClient
app = Flask(__name__)
PORT = 777
HOST = "10.93.48.142"
ADDR = (HOST, PORT)
HEADER = 64
FORMAT = "utf-8"

# connecting to the socket server
webClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webClient.connect(ADDR)


# define the method of send message and receive message
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    webClient.sendall(send_length)
    webClient.sendall(message)


def receive_reply(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg = ""
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg


# define the main route of the webpage
@app.route("/", methods=["GET", "POST"])
def main():
    # we set the message from web start with 'web'
    message = "web"
    schefeed = ["", "", ""]
    if request.method == 'POST':
        # when the schedule button pressed we send a message to request the schedule information from the socket server
        # then we receive the message and arrange them into the schedule table
        if request.form.get('schedule') == 'schedule':
            message += " schedule"
            send(message)
            data = receive_reply(webClient)
            print(data)
            sche = data.split(" ")
            for n in range(len(sche)):
                schefeed[n] += sche[n]
            print(schefeed)
            return render_template("index.html", sfeed1time=schefeed[0], sfeed2time=schefeed[1], sfeed3time=schefeed[2])
        # when the feed button pressed we append 'feed' to the message
        if request.form.get('feed') == 'feed':
            message += " feed"
        # when the clean button pressed we append 'clean' to the message
            message += " clean"
        # when the play button pressed we append 'play on' to the message
        if request.form.get('play') == 'play on':
            message += " play on"
        # when the play button pressed we append 'play off' to the message
        if request.form.get('play') == 'play off':
            message += " play off"
        # send the message to backend server
        send(message)
    return render_template("index.html")


# the route for setting page
@app.route("/setting", methods=["GET", "POST"])
def setting():
    # this for the starter of the update message
    message = "web update"
    if request.method == 'POST':
        # we get the information from the input on the website
        if request.form.get('submit_button') == 'Submit':
            message += " "
            message += request.form.get('numberOfTimes')
            message += " "
            if request.form.get('numberOfTimes') == '1':
                message += str(request.form.get('time1'))
            elif request.form.get('numberOfTimes') == '2':
                message += str(request.form.get('time1'))
                message += " "
                message += str(request.form.get('time2'))
            elif request.form.get('numberOfTimes') == '3':
                message += str(request.form.get('time1'))
                message += " "
                message += str(request.form.get('time2'))
                message += " "
                message += str(request.form.get('time3'))
            message += " "
            message += request.form.get('feedAmount')
            # arrange the setting information and send it to the backend server
            send(message)
            # after submit, the webpage jump back to the main page
            return redirect("/")
    return render_template("settingpage.html")


# the route for history page
@app.route("/history", methods=["GET", "POST"])
def history():
    # the starter of the history request message
    message = "web history"
    send(message)
    data = receive_reply(webClient)
    print(data)
    # the list to save information table
    feedhistime = [" ", " ", " ", " ", " "]
    feedhisamount = [" ", " ", " ", " ", " "]
    cleanhistime = [" ", " ", " ", " ", " ", " "]
    text = data.split(" clean ")
    feedlist = text[0].split(" ")
    print(feedlist)
    cleanlist = text[1].split(" ")
    print(cleanlist)
    lenfeed = len(feedlist)
    lenclean = len(cleanlist)
    numfeed = int(feedlist[1])
    numclean = int(cleanlist[0])
    # rendering the message into the format to fit in the website
    if numfeed > 5:
        for n in range(5):
            feedhistime[5 - n] += feedlist[lenfeed - 2 * n - 2]
            feedhisamount[5 - n] += feedlist[lenfeed - 2 * n - 1]
    elif numfeed > 0:
        for n in range(numfeed):
            feedhistime[n] += feedlist[lenfeed - 2 * n - 2]
            feedhisamount[n] += feedlist[lenfeed - 2 * n - 1]

    if numclean > 5:
        for n in range(5):
            cleanhistime[n] += cleanlist[lenclean - n]
    elif numclean > 0:
        for n in range(numclean):
            cleanhistime[n] += cleanlist[lenclean - n - 1]

    return render_template("history.html", feed1time=feedhistime[0], feed2time=feedhistime[1], feed3time=feedhistime[2],
                           feed4time=feedhistime[3], feed5time=feedhistime[4], feed1amount=feedhisamount[0],
                           feed2amount=feedhisamount[1], feed3amount=feedhisamount[2], feed4amount=feedhisamount[3],
                           feed5amount=feedhisamount[4], clean1time=cleanhistime[0], clean2time=cleanhistime[1],
                           clean3time=cleanhistime[2], clean4time=cleanhistime[3], clean5time=cleanhistime[4])


if __name__ == "__main__":
    app.run(debug=True, host="10.93.48.142", port=80)
