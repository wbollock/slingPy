# slingPY

Creating a schedule notifier (who is currently working) via the Sling Scheduler API. No Premium API functions used.

Designed for inclusion into a PHP file.

## Requirements

pip3 install -r requirements.txt

## Usage

1. Create file "apikeys.txt". Each API key on a seperate line.

E.g:

apikey1
apikey2
apikey3


2. Have a cron job run the program. 

Every 30 min

`*/30 * * * * support python3 /somedir/slingPy.py`

3. Then, if you want to display it on a PHP page, add the following line to your PHP code:

`include 'slingPy/working.php';`

`<?php include 'slingPy/working.php'; ?>`

(For OsTicket, add to ~ line 8 of footer.php.inc)
(public_html/include/staff/footer.inc.php)
