import requests, time, os, string, random

baseUrl = "https://inboxes.com/api/v2"
globalHeaders = {
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'Referer': 'https://inboxes.com/',
    'sec-ch-ua-mobile': '?1',
    'authorization': 'Bearer null',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua-platform': '"Android"',
}
globalHeaders2 = globalHeaders.copy()
del globalHeaders2["authorization"]

def banner():
    os.system("clear")
    banner = " ___       _\n|_ _|_ __ | |__   _____  __\n | || '_ \\| '_ \\ / _ \\ \\/ /\n | || | | | |_) | (_) >  < \n|___|_| |_|_.__/ \\___/_/\\_\\\n============================================="
    print(banner)

def firstView():
    banner()
    print("01. Lihat list email")
    print("02. Buat email baru")
    inpt = ""
    while True:
        print("=============================================")
        inpt = input("??. Pilih: ")
        print("=============================================")
        if inpt not in ["1", "01", "2", "02"]:
            print("!!. Pilihan tidak ada")
        else:
            inpt = str(int(inpt))
            break
    if inpt == "1":
        listEmail()
    elif inpt == "2":
        buatEmail()

def listEmail():
    banner()
    if "email.list" not in os.listdir():
        open("email.list", "w").write("[]")
        print("!!. Anda belum membuat email")
        time.sleep(2)
        firstView()
    else:
        dataEmail = eval(open("email.list", "r").read())
        if len(dataEmail) == 0:
            print("!!. Anda belum membuat email")
            time.sleep(2)
            firstView()
        else:
            print("**. Daftar email anda")
            print("=============================================")
            nomorEmail = []
            for email in enumerate(dataEmail):
                nomorEmail.append(str(email[0] + 1))
                if email[0] < 9:
                    nomorEmail.append("0" + str(email[0] + 1))
                print(f"{'0' + str(email[0] + 1) if email[0] < 9 else str(email[0] + 1)}. {email[1]}")
            print("=============================================")
            print("**. Pilih untuk melihat inbox.")
            inpt = ""
            while True:
                inpt = input("??. Pilih: ")
                print("=============================================")
                if inpt not in nomorEmail:
                    print("!!. Pilihan tidak ada")
                else:
                    inpt = int(inpt) - 1
                    break
            lihatInbox(dataEmail[inpt])


def buatNamaRandom():
    return "".join(random.choice(f"{string.ascii_lowercase}") for i in range(15)) + f"@{random.choice(getDomainList())}"

def getDomainList():
    req = requests.get(f"{baseUrl}/domain", headers=globalHeaders2).json()
    return [domain["qdn"] for domain in req["domains"]]


def buatEmail():
    banner()
    print("01. Nama random")
    print("02. Nama custom")
    inpt = ""
    while True:
        print("=============================================")
        inpt = input("??. Pilih: ")
        print("=============================================")
        if inpt not in ["1", "01", "2", "02"]:
            print("!!. Pilihan tidak ada")
        else:
            inpt = str(int(inpt))
            break
    if inpt == "1":
        email = buatNamaRandom()
        create(email)
    else:
        username = ""
        domain = ""
        while True:
            username = input("**. Masukkan username (minimal 10 karakter): ")
            print("=============================================")
            if len(username) < 10:
                print("!!. Minimal 10 karakter")
            else:
                break
        domainList = getDomainList()
        for i in enumerate(domainList):
            print(f"{'0' + str(i[0] + 1) if i[0] < 9 else str(i[0] + 1)}. {i[1]}")
        while True:
            print("=============================================")
            dom = input("??. Pilih domain: ")
            print("=============================================")
            if dom.isdigit() and int(dom) > 0 and int(dom) <= len(domainList):
                domain = domainList[int(dom) - 1]
                break
            else:
                print("!!. Pilihan tidak ada")
        email = f"{username}@{domain}"
        create(email)
    print("**. Ingin melihat inbox (y/t): ")
    inpt = ""
    while True:
        inpt = input("??. Pilih: ")
        if inpt not in ["y", "Y", "t", "T"]:
            print("!!. Pilihan tidak ada")
        else:
            inpt = inpt.lower()
            break
    if inpt == "y":
        lihatInbox(email)
    else:
        firstView()


def lihatInbox(email):
    banner()
    print(f"**. Menampipkan kotak masuk untuk email {email}")
    print("**. Pilih nomor pesan untuk membuka pesan")
    print("**. Pilih r/b untuk refresh/kembali")
    print("=============================================")
    inpt = False
    inbList = getRequest(email)["msgs"]
    if len(inbList) == 0:
        print("**. Belum ada pesan masuk")
    else:
        for i in enumerate(inbList):
            nomor = "0" + str(i[0] + 1) if len(str(i[0])) == 1 else str(i[0] + 1)
            print(f"{nomor}. Dari: {i[1]['f']}, Subjek: {i[1]['s']}, {i[1]['rr']}")
    while True:
        inpt = input("??. Pilih: ")
        if inpt.isdigit():
            if int(inpt) < 1 or int(inpt) > len(inbList):
                print("!!. Pilihan tidak ada")
            else:
                lihatPesan(inbList[int(inpt) - 1]["uid"], email)
                inpt=False
                break
        else:
            if inpt.lower() == "r":
                inbList = getRequest(email)["msgs"]
                if len(inbList) == 0:
                    print("**. Belum ada pesan masuk")
                else:
                    for i in enumerate(inbList):
                        nomor = "0" + str(i[0] + 1) if i[0] < 9 else str(i[0] + 1)
                        print(f"{nomor}. Dari: {i[1]['f']}, Subjek: {i[1]['s']}, {i[1]['rr']}")
            elif inpt.lower() == "b":
                inpt == True
                break
            else:
                print("!!. Pilihan tidak ada")
    if inpt:
        firstView()

def lihatPesan(uid, email):
    banner()
    print(f"**. Menampilkan pesan dipilih")
    print(f"**. email {email}")
    print(f"**. uid message {uid}")
    print("=============================================")
    getMessage = requests.get(f"{baseUrl}/message/{uid}").json()
    print(f"**. Dari: {getMessage['f']}")
    print(f"**. Subjek: {getMessage['s']}")
    print(f"**. Pesan: {getMessage['text']}")
    print("=============================================")
    input("[ENTER UNTUK KEMBALI KE MENU UTAMA]")
    firstView()

def create(email):
    createMail = getRequest(email)
    emailList = eval(open("email.list", "r").read())
    emailList.append(email)
    open("email.list", "w").write(str(emailList))
    print(f"**. Email {email} berhasil dibuat & disimpan")

def getRequest(email):
    return requests.get(f"{baseUrl}/inbox/{email}", headers=globalHeaders).json()


if __name__ == "__main__":
    firstView()
