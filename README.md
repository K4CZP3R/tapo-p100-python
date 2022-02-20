# tapo-p100-python
Work in progress implementation of tapo protocol in python.

Writeup here: https://k4czp3r.xyz/reverse-engineering/tp-link/tapo/2020/10/15/reverse-engineering-tp-link-tapo.html

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

To do list

- [x] Handshake
- [x] Encrypt data
- [x] Login request
- [x] Decrypt data
- [x] Change state

# How to install it (Linux)
1. Make venv: `python3 -m venv venv`
2. Activate venv: `source venv/bin/activate`
3. Install wheel: `pip install wheel`
4. Install requirements `pip install -r req.txt`

# How to install it (Windows)
TODO

# How to use it
```
usage: main.py [-h] TPLINK_EMAIL TPLINK_PASS ADDR STATE

Change plug state.

positional arguments:
  TPLINK_EMAIL  Your TPLink account email
  TPLINK_PASS   Your TPLink account password
  ADDR          Address of your plug (ex. 192.168.2.22)
  STATE         New state of the plug (on=1 off=0)

optional arguments:
  -h, --help    show this help message and exit
```

Example: `python main.py email@gmail.com Password123 192.168.137.135 1`

---
[buymecoffee]: https://www.buymeacoffee.com/k4czp3r
[buymecoffeebadge]: https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png
