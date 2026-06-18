Score_English = int(input("คะแนนอังกฤษคุณได้เท่าไหร่? "))
Score_Math = int(input("คะแนนคณิตคุณได้เท่าไหร่? "))
Score_Science = int(input("คะแนนวิทยาศาสตร์คุณได้เท่าไหร่? "))
total_score = (Score_English + Score_Math + Score_Science)
average = total_score/3
print("คะแนนรวม3วิชาได้", total_score, "คะแนน")
print ("คะแนนเฉลี่ยของคุณทั้ง 3 วิชาคือ", average, "คะแนน")
if average >=80 :
    print("ดีเยี่ยม")
elif average >=60 :
    print("ผ่าน")
else:
    print("ควรปรับปรุง")