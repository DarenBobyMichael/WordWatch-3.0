import subprocess

if __name__=="__main__":
    while 1:
        selection = int(input("\nSelect the medium to detect\n===========================\n\t1. Text\n\t2. Audio\n\t3. Video\n\t4. Exit\n===========================\n: "))
        if selection==1:
            subprocess.run("cls",shell=True)
            print("TEXT ANALYZER\n===========\n")
            subprocess.run(["python","malayalam_preditct.py"])
        elif selection==2:
            subprocess.run("cls",shell=True)
            print("AUDIO ANALYZER\n===========\n")
            subprocess.run(["python","malayalam_preditct_audio.py"])

        elif selection==3:
            subprocess.run("cls",shell=True)
            print("VIDEO ANALYZER\n===========\n")
            subprocess.run(["python","malayalam_preditct_video.py"])
        elif selection==4:
            exit(1)
        else:
            print("\nInvalid option")
    

        
    