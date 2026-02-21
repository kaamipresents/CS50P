print("Logger module loaded")

count = 0

def log(message):
    global count
    count += 1
    print(f"[{count}] {message}")

if __name__ == "__main__":
    print("Logger running as main")
    log("Test message")