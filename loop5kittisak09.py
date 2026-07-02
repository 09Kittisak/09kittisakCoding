print(">>>>>เกมทายตัวเลข<<<<<")
import random
answer = random.randint(1,101)
count = 0

while True:
    Number = int(input("ใส่ตัวเลขที่คุณทาย1-100?  "))
    count +=1

    if Number<answer:
        print("น้อยไปทายใหม่  ")
    elif Number>answer:
        print("มากไปทายใหม่  ")
    else:
        print("ถูกต้อง")
        print("คุณทายทั้งหมด", count, "ครั้ง")
        break