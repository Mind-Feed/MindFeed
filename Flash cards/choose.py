choose = int(input("Flash Cards Reviewer\n[1] Test\n[2] Add\n[3] View\n[4] Exit\n"))

while True:
  if choose == 1:
    Test()
  elif choose == 2:
    Add()
  elif choose == 3:
    View()
  elif choose == 4:
    exit()
  else:
    print("try again")
    choose = int(input("[1] Test\n[2] Add\n[3] View\n[4] Exit\n"))