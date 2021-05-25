
from queue import Queue
from datetime import datetime, timedelta
import django,os,time,asyncio,smtplib,requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CowinNotifier.settings')
django.setup()

from notifier.models import Pin,Order,Email


schedule = Queue(maxsize = 3000)
in_queue=set()
class mail:
  def __init__(self, pin, message):
    self.pin = pin
    self.message = message

async def checkAvailability():
    num_days = 2
    actual = datetime.today()
    list_format = [actual + timedelta(days=i) for i in range(num_days)]
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
    all_pin=Pin.objects.all()
    pincodes = list(all_pin)
    # print(all_pin)
    for i in pincodes:
        # print(type(i.pin))
        counter=0
        pincode=i.pin
        for given_date in actual_dates:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
                header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
                
                result = requests.get(URL, headers=header)

                if result.ok:
                    response_json = result.json()
                    if response_json["centers"]:
                        message=""
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["available_capacity"] > 0 ) :
                                    counter=counter+1
                                    message="\n"+message
                                    message+= " " + "Pincode: " + pincode
                                    message+= " " + "\t"+"Available on: {}".format(given_date)
                                    message+= " " + "\t" + center["name"]
                                    message+= ", "  + center["block_name"]
                                    message+= " " + "\t Price: " + center["fee_type"]
                                    message+= " " + "\t Availablity : " + str(session["available_capacity"])

                                    if(session["vaccine"] != ''):
                                        message+= " " + "\t Vaccine type: "+ str(session["vaccine"])
                                    message+= " " + "\n"

        if counter!=0 or pincode=="462003":
            obj=mail(pincode,message) 
            if obj not in in_queue:
                schedule.put(obj)
                in_queue.add(obj)               
                print("scheduled mails to "+pincode)
                await asyncio.sleep(4)

    return None

async def sendEmail():
    if schedule.empty():
        return 1

    obj=schedule.get()
    in_queue.remove(obj)
    availablePin=obj.pin
    response=obj.message
      
    ordersForPin=Order.objects.filter(pin=availablePin)
    all_orders=list(ordersForPin)

    #if no orders are ther then delete pin from Pin
    # print(all_orders)
    if len(all_orders) == 0:
        del_pin=Pin.objects.filter(pin=availablePin)
        del_pin.delete()
        return 0
    else:
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
       
        your_email = "your_password"
        your_password = "your_email"
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(your_email, your_password)
 

        for order in all_orders:
            print(order.email)
            reciever_email= order.email

            msg = MIMEMultipart()
            msg['To'] = reciever_email
            msg['From'] = your_email
            msg['Subject'] = "Vaccine Slots available at pin: " +availablePin
            body=response
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()

            #send email
            try:
                server.sendmail(your_email,reciever_email,text)
                # print('Email to ',reciever_email,'successfully sent!\n\n')
            except Exception as e:
                print('Email to ',reciever_email,'could not be sent :( to\n\n')

            #save in eamil
            e= Email(pin=availablePin,email=reciever_email)
            e.save()

            #delete order from Order
            del_ob= Order.objects.filter(id=order.pk)
            del_ob.delete()
            await asyncio.sleep(2)

        server.quit()
        del_pin=Pin.objects.filter(pin=availablePin)
        del_pin.delete()

    


    
    return None


async def main():
    
    while True:
        t0 = time.time()
        await asyncio.wait( [
            checkAvailability(),
            sendEmail(),
            ] )
        t1 = time.time()
        print('Took %.2f ms' % (1000*(t1-t0)))

        # To save resources on server sleep whole script for 3 minute 
        time.sleep(60*3)
    
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#loop.close()