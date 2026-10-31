from functions.get_file_content import get_file_content


def test() -> None:
    file = "lorem.txt"
    result = get_file_content("calculator", file)
    print(f"{file}t length: {len(result)}")
    print(f"{file} truncated: {'truncated' in result}")
    print("")

    file = "main.py"
    result = get_file_content("calculator", file)
    print(result)
    print("")

    file = "pkg/calculator.py"
    result = get_file_content("calculator", file)
    print(result)
    print("")

    file = "/bin/cat"
    result = get_file_content("calculator", file)
    print(result)
    print("")

    file = "pkg/does_not_exist.py"
    result = get_file_content("calculator", file)
    print(result)
    print("")


if __name__ == "__main__":
    test()
