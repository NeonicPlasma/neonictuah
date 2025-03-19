def check_string (s):

    validKey = True

    if (len(s) < 6 or len(s) > 12):
        print("Not a valid key -- too long / too short")
        validKey = False

    
        