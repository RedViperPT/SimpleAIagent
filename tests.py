from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

# tests get_file_info
# def test_get_files_info():
#     test_cases = [
#         ("calculator", "."),
#         ("calculator", "pkg"),
#         ("calculator", "/bin"),
#         ("calculator", "../")
#     ]
    
#     for working_dir, directory in test_cases:
#         print(f"Result for '{directory}' directory:")
#         result = get_files_info(working_dir, directory)
#         print(result)
#         print()  

# tests get_file_content
# def test():
#     print(get_file_content("calculator", "main.py"))

#     print(get_file_content("calculator", "pkg/calculator.py"))

#     print(get_file_content("calculator", "/bin/cat"))


# tests write_file
def test_write_file():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
if __name__ == "__main__":
    test_write_file()
