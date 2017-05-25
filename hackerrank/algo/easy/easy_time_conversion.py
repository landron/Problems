# http://www.hackerrank.com/challenges/time-conversion

def resolve(time):
    result = ""
    hour = time[:time.find(':')]
    if time[-2:] == "AM":
        result = time[:-2]
        result = time[:-2] if hour != "12" else "00" + time[2:-2]
    elif hour != "12":
        result = str(12+int(hour)) + time[2:-2]
    else:
        result = time[:-2]
    return result

def debug_validations():
    assert resolve("07:05:45PM") == "19:05:45"
    assert resolve("12:05:45PM") == "12:05:45"
    assert resolve("12:05:45AM") == "00:05:45"

def read_input():
    return input().strip()

def main():
    debug_validations()
    # time = read_input()
    print(resolve("12:05:45PM"))

if __name__ == "__main__":
    main()
