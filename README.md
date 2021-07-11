# Project : Intellup

### Deployment has been removed.

#### Project is live in [http://3.7.232.152/](http://3.7.232.152/)
You can simply login by this accounts or register a new one.
Dummy Accounts :
```
Username : user1
Password : 12345

Username : user2
Password : 12345
```

You can visit admin panel located at [http://3.7.232.152/admin/](http://3.7.232.152/admin/)

Admin login details :
```
Username : admin
Password : 123456
```

# Description
### What problem we are solving ?
=> We all know how boring it is to wake up in the morning and attend lectures online. It even hurts more to give an exam online, even more when it is a competitive exam we are preparing for. We all agree that learning has quite a boring and monotonous task now.

On a parallel perspective, according to research, an average class 9 student spends 3 hours of his time every day online, most of it is spent in playing games or watching random videos, which in no way contributes to his academic growth.


Online education had reduced student to student interaction. Sitting all day long in front of a laptop attending online lectures had reduced competitiveness among students. To succeed in a competitive exam, students need to get a taste for it from childhood. Our application helps to build a competitive nature among students which will help them in future. Students can battle with other participants throughout the world sitting at their home and prizes that they will get will motivate them. It’s human psychology that if we get rewards we perform better.


### Solution 
=> It’s human physiology that we perform better in groups especially when we are competing with others. In today’s world where everything is online students need a platform where they can compete with others to know their true potential and can work to improve it. 


We have built a platform, where any student can choose his subject and accordingly he/she can participate in various contests. Even he/she can compete with his/her friends or opponents in realtime.

We are introducing the microtransaction system in this. A student can compete and get rewards in form of cash or vouchers.To start the game we are providing a bunch of coins which can be used in battle or contest to earn coins which can be converted to cash or vouchers .

Thus we have gamified the process of learning hoping to make a more enriched and creative future



# Demo (Click On This 👇 Pic To Open Video)

[![Intellup Demo](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/video.gif)](https://youtu.be/6-EcysQV_uU "Intellup Demo")

[For More Info Check This Presentation](https://raw.githubusercontent.com/Tanmoy741127/Intellup/f3de96e4407a88e2bb4cfe97b79a74444c55c767/screenshots/presentation.pdf)


# Project Components

1. Frontend
	- HTML
	- CSS
	- Javascript
	- Jquery

2. Backend
	- Django
	- NodeJS

# Installation
##### Prerequisites
- Python
- Nodejs
- Redis Server
-  MongoDB Database

##### Steps:
1.Start Redis Server

```
Open an terminal and run
redis-server
```

2.Create a database in mongodb . Name : "edugame" 

3.Go to the edugame_realtime folder and run this commands

```
npm install
node index.js

```
4.Go to edugame-backend folder
5.First configure the enviroment variables [./edugame/.env]

```
SECRET_KEY='django-insecure-)lu%mn4^zn5##9y0j-a4rpo)2a2@t)ipxn8#^a5*t0es)j1w5f'
MAILGUN_ENDPOINT=''
MAILGUN_API=''
RAZORPAY_KEY_ID=''
RAZORPAY_KEY_SECRET=''
```
> We are using mailgun as our mail service , So we need to collect the API keys and Endpoint from its dashboard. Secondly, we need Razorpay payment gateway . We need to collect the API keys from Razorpay Dashboard

6.Create a Virtualenv & Activate
```
python -m venv env
source env/bin/activate
```
7.Install necessary packages
```
pip install -r requirements.txt
```
8.Run database migration
```
python manage.py makemigrations datahandler
python manage.py makemigrations
python manage.py migrate datahandleer
python manage.py migrate
```

9.Run Django Server
```
python manage.py runserver
```

It will start server in **127.0.0.1:8000**

### Screenshots
> Homepage

![Homepage](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/1.png)

> Choose Battle

![Choose Battle](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/2.png)

> Battle Rules & Info Page

![Battle Info Page](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/3.png)

> Battle Page

![Battle Page](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/4.png)

> Contest List Page

![Contest Page](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/7.png)

> Leaderboard

![Leaderboard](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/8.png)

> Profile Page

![Profile Page](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/9.png)

> Wallet

![Wallet](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/10.png)

> Performance Stats 

![Performance Stats ](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/11.png)

> Coin Recharge

![Coin Recharge](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/12.png)

> Admin Panel Overview

![Admin Panel](https://raw.githubusercontent.com/Tanmoy741127/Intellup/main/screenshots/6.png)

## License
[BSD 3-Clause "New" or "Revised" License](https://github.com/Tanmoy741127/Intellup/blob/main/LICENSE)
