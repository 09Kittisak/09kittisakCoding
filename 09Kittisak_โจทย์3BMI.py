print("โปรแกรมคำนวณค่าBMI")
Weight = int(input("\nกรอกตัวเลขน้ำหนักของคุณ "))
Height = float(input("กรอกตัวเลขส่วนสูงของคุณ "))

print(("\nส่วนสูงของคุณคือ"), Height, ("เมตร"))
print(("น้ำหนักของคุณคือ"), Weight, ("กิโลกรัม"))
BMI = Weight/(Height * Height)
print(("\nค่าBMIของคุณคือ"), BMI , ("หน่วย"))
if BMI <18.5:
    print("น้ำหนักน้อย")
elif BMI <22.9:
    print("ปกติ")
elif BMI <24.9:
    print("น้ำหนักเกิน")
else:
    print("อ้วน")
