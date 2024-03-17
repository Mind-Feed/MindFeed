file = open( "Flash cards/cards.txt", "a" )
def Add():
  while True:
    question = input( "name: " )
    answer = input( "means: " )
    file.write( f"{question},{answer}\n" )
    exit()
    create.close()

def View():
    with open('Flash cards/cards.txt', 'r') as file:
        line_count = 0
        print("[ENTER] show more \n[q] to quit")
        while True:
            line = file.readline()
            if not line:
                break
            values = line.strip().split(",")
            
            print(f'name {values[0]} means {values[1]}')
            line_count += 1
            if line_count % 2 == 0:
                if input().lower() == 'q':
                    break

choose = int(input("Flash Cards Reviewer\n[1] Test\n[2] Add\n[3] View\n[4] Exit\n"))

while True:
  if choose == 1:
    print("Under maintinance")
  elif choose == 2:
    Add()
  elif choose == 3:
    View()
    choose = int(input("[1] Test\n[2] Add\n[3] View\n[4] Exit\n"))
  elif choose == 4:
    exit()
    
