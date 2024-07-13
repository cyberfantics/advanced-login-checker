# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:41:03 2024

@author: Mansoor
"""

import paramiko
import telnetlib
import ftplib
import requests
import threading
import logging
from queue import Queue

# Configure logging
logging.basicConfig(filename='login_attempts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ssh_login(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        ssh_session = ssh.get_transport().open_session()

        if ssh_session.active:
            logging.info(f"SSH Login Successful on {host}:{port} with username {username} and password {password}")
            return True
    except Exception as e:
        logging.warning(f"SSH Login Failed: {e}")
    finally:
        ssh.close()
    return False

def telnet_login(host, port, username, password):
    try:
        tn = telnetlib.Telnet(host, port)
        tn.read_until(b"Login: ")
        tn.write(username.encode('utf-8') + b'\n')
        tn.read_until(b"Password: ")
        tn.write(password.encode('utf-8') + b'\n')

        result = tn.expect([b"Last Login"], timeout=2)
        if result[0] >= 0:
            logging.info(f"Telnet Login Successful on {host}:{port} with username {username} and password {password}")
            return True
    except EOFError:
        logging.warning(f"Telnet Login Failed for {username}")
    except Exception as e:
        logging.error(f"Telnet Error: {e}")
    finally:
        tn.close()
    return False

def ftp_login(host, username, password):
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user=username, passwd=password)
        logging.info(f"FTP Login Successful on {host} with username {username} and password {password}")
        ftp.quit()
        return True
    except Exception as e:
        logging.warning(f"FTP Login Failed: {e}")
    return False

def http_login(host, username, password):
    url = f"http://{host}"
    try:
        response = requests.get(url, auth=(username, password))
        if response.status_code == 200:
            logging.info(f"HTTP Login Successful on {url} with username {username}")
            return True
        else:
            logging.warning(f"HTTP Login Failed: {response.status_code}")
    except Exception as e:
        logging.error(f"HTTP Error: {e}")
    return False

def login_attempts(queue, host):
    while not queue.empty():
        username, password = queue.get()
        ssh_login(host, 22, username, password)
        telnet_login(host, 23, username, password)
        ftp_login(host, username, password)
        http_login(host, username, password)
        queue.task_done()

def main():
    host = input("Enter the host address: ")
    with open("default.txt", "r") as f:
        queue = Queue()
        for line in f:
            vals = line.split()
            if len(vals) < 2:
                print("Invalid line in credentials file, skipping.")
                continue
            
            username = vals[0].strip()
            password = vals[1].strip()
            queue.put((username, password))

        # Start threads for concurrent login attempts
        for _ in range(5):  # Number of concurrent threads
            thread = threading.Thread(target=login_attempts, args=(queue, host))
            thread.start()

        queue.join()  # Wait for all tasks to finish

if __name__ == "__main__":
    main()
