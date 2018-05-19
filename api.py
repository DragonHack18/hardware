import urllib.request

"""Just a redundant python file where I test an API request"""

contents = urllib.request.urlopen("http:127.0.0.1/walletWall/public/api/paymentapproved").read()
