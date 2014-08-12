if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaters.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

def counter(FirstNumber, LastNumber):
    #Base Check
    if FirstNumber <= LastNumber:
        #Pallindromic Prime check
        if PrimeNumber(FirstNumber, 2) and question1.PalinCheck(FirstNumber):
            print(FirstNumber)
        counter(FirstNumber+1, LastNumber)