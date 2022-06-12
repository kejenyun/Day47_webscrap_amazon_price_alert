from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os

URL= "https://www.amazon.ca/dp/B091M91SB3/?coliid=IQGUHGMO0PQ9U&colid=14WWARX76XG5J&psc=1&ref_=lv_ov_lig_dp_it"

#scrapping

response = requests.get(url=URL, headers={'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
webpage =response.text
#print(webpage)

soup = BeautifulSoup(webpage, "lxml")
#print(soup.prettify())
price =soup.select_one(".a-offscreen").getText()
price_without_currency = price.split("$")[1]
price_float=float(price_without_currency)
print (price_float)
product_name = soup.select_one("#productTitle").getText()

# Sent email
my_email = os.environ.get('my_email')
password = os.environ.get('password')
to_email = os.environ.get('to_email')

BUY_PRICE =100

if price_float < BUY_PRICE:
    connection = smtplib.SMTP("smtp.mail.yahoo.com", port=587)
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=to_email,
                        msg=f"Subject:Price Drop\n\n {product_name} is now ${price_float}\n\n{URL}"
                        )
    connection.close()