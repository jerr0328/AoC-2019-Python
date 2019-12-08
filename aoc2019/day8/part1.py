from . import check_image, parse_string


def main():
    with open("data/8.txt", "r") as f:
        img_str = f.read().strip()
    img = parse_string(img_str, 25, 6)
    print(check_image(img))


if __name__ == "__main__":
    main()
