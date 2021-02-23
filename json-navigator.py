from json import load

def navigator(path: str) -> None:
    """
    Helps to navigate through json file.
    """
    with open(path) as dzhson:
        obj = load(dzhson)
    path = []
    while True:
        currObject = obj
        for i in path:
            currObject = currObject[i]
        currPath = ''
        for i in path:
            currPath += str(i) + '>>' 
        if isinstance(currObject, list):
            print('This is list. Do you want to display entire list? (yes/no)\n\n')
            check = ''
            while check not in ('yes', 'no'):
                check = input(">> ")
            if check == 'yes':
                lst = ''
                for i in currObject:
                    lst += str(i) + '  '
                print(lst)
            else:
                break
            item = -1
            while int(item) not in range(1, len(lst)+1):
                try:
                    item = int(input('Enter number in range from 1 to %s\n\n>> ' % str(len(lst)+1)))
                except ValueError:
                    pass
            path.append(int(item))
            print()
        if isinstance(currObject, dict):
            print("This is a dict. Enter key from next list.\n\n")
            dct = ''
            for key, value in currObject.items():
                dct += key + '  '
            print(dct)
            kluch = ''
            while kluch not in currObject:
                kluch = input(">> ")
            path.append(kluch)
            print()
        if isinstance(currObject, int) or isinstance(currObject, str):
            print("This is string. Do you want to dispay it? (yes/no)\n\n")
            check = ''
            while check not in ('yes', 'no'):
                check = input(">> ")
            if check == 'yes':
                print(currObject)
            print('\n\nThis is the end of file. Do you want to go back? (yes/no)')
            check = ''
            while check not in ('yes', 'no'):
                check = input(">> ")
            if check == 'yes':
                print()
                path = path[:-1]
            else:
                break
        elif currObject is None:
            print('\n\nThis is None object. Do you want to go back? (yes/no)')
            check = ''
            while check not in ('yes', 'no'):
                check = input(">> ")
            if check == 'yes':
                path = path[:-1]
            else:
                break

if __name__ == "__main__":
    path = ''
    while True:
        try:
            path = input("Enter path to file: ")
            navigator(path)
        except FileNotFoundError:
            print("File not found. Try again")
            pass
