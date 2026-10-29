from functions.run_python_file import run_python_file


def test(working_dir, file_path, args=None):
    print(f'Test ("{working_dir}", "{file_path}", "{args}")')
    print(run_python_file(working_dir, file_path, args))
    print()


test("calculator", "main.py")
test("calculator", "main.py", ["3 + 5"])
test("calculator", "tests.py")
test("calculator", "../main.py")
test("calculator", "nonexistent.py")
test("calculator", "lorem.txt")
