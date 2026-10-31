from functions.get_files_info import get_files_info


def test() -> None:
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    directory = "pkg"
    result = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:")
    print(result)
    print("")

    directory = "/bin"
    result = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:")
    print(result)
    print("")

    directory = "../"
    result = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:")
    print(result)


if __name__ == "__main__":
    test()
