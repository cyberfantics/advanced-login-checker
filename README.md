# Advanced Login Checker

This Python script automates the process of testing multiple login credentials against various protocols, including SSH, Telnet, FTP, and HTTP. The user can specify the host and choose to save the results via input prompts.

## Features

- **Concurrent Login Attempts:** Utilizes multi-threading to perform login attempts simultaneously, improving efficiency.
- **Protocol Support:** Supports SSH, Telnet, FTP, and HTTP authentication.
- **Detailed Logging:** Logs all attempts (successful and failed) to a file for review and analysis.
- **Input Validation:** Ensures that the credentials file is properly formatted before attempting logins.

## Requirements

- Python 3.x
- paramiko
- requests

## Installation

Clone the repository:

```bash
git clone https://github.com/cyberfantics/advanced-login-checker.git
cd advanced-login-checker
```

Install the required libraries:

```bash
pip install paramiko requests
```

## Usage
Run the Script:
```bash
python advanced_login_checker.py
```

1. **Enter the host:** When prompted, enter the host address you want to test the credentials against.
2. **Save the output:** The script automatically logs the results of the login attempts to login_attempts.log.

## Example
```Enter the host address: 192.168.1.1```
**This will perform login attempts using the credentials provided in default.txt and log the results to login_attempts.log.**

## Contact
Created by SalfiHacker - [GitHub](https://github.com/cyberfantics)

