from . import flatten_image, parse_string


def main():
    with open("data/8.txt", "r") as f:
        img_str = f.read().strip()
    img = parse_string(img_str, 25, 6)
    for line in flatten_image(img):
        print("".join(map(lambda x: "█" if x else " ", line)))


if __name__ == "__main__":
    main()
