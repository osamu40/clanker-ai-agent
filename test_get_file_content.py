from functions.get_file_content import get_file_content


def test_get_file(dir, file):
    result = get_file_content(dir, file)

    header_string = f"result = get_file_content({dir}, {file})"
    length_string = f"{file} length: {len(result)}"
    truncated_string = f"{file} truncated: {'truncated' in result}"

    result_string = ("\n").join([header_string, length_string, truncated_string])

    print(result_string)
    if file != "lorem.txt":
        print(result)
    print("\n========================\n")


test_get_file("calculator", "lorem.txt")
test_get_file("calculator", "main.py")
test_get_file("calculator", "pkg/calculator.py")
test_get_file("calculator", "/bin/cat")
test_get_file("calculator", "pkg/does_not_exist.py")
