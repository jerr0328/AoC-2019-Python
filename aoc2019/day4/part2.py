from . import valid_password


def main():
    valid_passwords = 0
    for password in range(248345, 746315):
        if valid_password(password, check_run=True):
            valid_passwords += 1
    print(valid_passwords)


if __name__ == "__main__":
    main()
