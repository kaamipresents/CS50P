import logger

print("Service module loaded")

def process():
    logger.log("Processing started")

if __name__ == "__main__":
    print("Service running as main")
    process()