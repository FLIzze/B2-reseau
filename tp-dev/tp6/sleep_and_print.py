import time

def count():
    for i in range(1,11):
        print(i)
        time.sleep(0.5)
        
def main():
   count() 
   count() 

if __name__ == "__main__":
    main()
