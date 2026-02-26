from main import dashify

def test_default():
    assert dashify("Kamran Mushtaq") == "kamran-mushtaq"
    assert dashify("   dashboard    game") == "dashboard-game"
    print("All tests passed")

def main():
    test_default()

if __name__ == "__main__":
    main()