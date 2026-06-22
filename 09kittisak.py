print("โปรแกรมแสดงคะแนนสอบ\n")

Score_English = int(input("คะแนนอังกฤษคุณได้เท่าไหร่? "))
Score_Math = int(input("คะแนนคณิตคุณได้เท่าไหร่? "))
Score_Science = int(input("คะแนนวิทยาศาสตร์คุณได้เท่าไหร่? "))

Total_Score = (Score_English + Score_Math + Score_Science)
Average = (Total_Score/3)
print("\nคะแนนรวมทั้ง 3 วิชา", Total_Score, "คะแนน")
print("คะแนนเฉลี่ยรวมทั้ง 3 วิชา", Average, "คะแนน")

if Average <60:
    print("\nควรปรับปรุง")
elif Average <80:
    print("\nผ่าน")
else:
     print("\nดีเยี่ยม")

print("\n นายกิตติศักดิ์ ไทพนา ม.4/4 เลขที่ 9 ")