from PIL import Image
from pyzbar.pyzbar import decode
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import pymysql

db = pymysql.connect(
    host="localhost",
    user="imran",
    passwd="12345",
    database="mydatabase"
)
mycursor = db.cursor()
sql="SELECT * FROM students "
mycursor.execute(sql)
result=mycursor.fetchall()
mycursor = db.cursor()
sql="SELECT * FROM students WHERE id"
mycursor.execute(sql)
result=mycursor.fetchall()
db.commit()
db.close()
st=[]
for i in result: 
    for j in i:
        st.append(str(j))

cam = PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.IN)
GPIO.setup(18,GPIO.OUT, initial=GPIO.LOW)


data=''
GPIO.output(18,GPIO.HIGH)
def main():
    while True:
        if GPIO.input(17)==1:
            print('Motion')
            cam.start_preview()
            sleep(3)
            cam.capture('/home/pi/Desktop/qrcode/image.png')
            cam.stop_preview()
            data = decode(Image.open('/home/pi/Desktop/qrcode/image.png'))
            if data:
                data=str(data[0][0])
                d=data[2:len(data)-1]
                if d in st:
                    print('valid user '+d)
                    GPIO.output(18,GPIO.LOW)
                    sleep(3)
                    GPIO.output(18,GPIO.HIGH)
                else:
                    print('Invalid '+d)
            else:
                print('Invalid')
                pass

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        cam.stop_preview()
        print('Exit')
