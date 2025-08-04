with open('example.txt', 'w') as f :
    f.write('hello world\nThis is an automated message.')

with open ('example.txt', 'r') as f :
    content = f.read()
    print(content)