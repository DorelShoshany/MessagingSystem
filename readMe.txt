The server run on: http://ec2-18-185-241-68.eu-central-1.compute.amazonaws.com:8080/

But, if you want your own local serevr:
**all the insreaction are for linux**

Install/update python 3.7:
	alias python='/usr/bin/python3.7'
	. ~/.bashrc
	sudo yum install python37 python37-pip

Install git:
	sudo yum install git

Clone the project from the gitHub:
	git clone https://github.com/DorelShoshany/MessagingSystem

Run the server:
	cd MessagingSystem
	sudo pip3 install --no-cache-dir -r requirements.txt
	sudo pip3 install python-dotenv
	venv\scripts\activate
	python main.py
	Running on http://0.0.0.0:8080/



