import csv
from tempfile import NamedTemporaryFile
import shutil
import secrets
import string

from platform import python_version

fileMailPassword = 'users.csv'
tempFile = NamedTemporaryFile('w+t', newline='', delete=False)
createCMD = open('psonoCMD.txt', 'w')

alphabet = string.ascii_letters + string.digits

if __name__ == '__main__':
    with open(fileMailPassword) as csvFile, tempFile:
        reader = csv.DictReader(csvFile, delimiter=';')
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(tempFile, fieldnames=fieldnames, delimiter=';', )
        writer.writeheader()

        for row in reader:
            if ((row['User created'] != 'Yes') and (row['Email'] != '')):
                row['Pass'] = ''.join(secrets.choice(alphabet) for i in range(10)) # 10-character password
                createCMD.write('python3 ./psono/manage.py createuser ' + row['Email'] + ' ' + row['Pass'] + ' ' + row['Email'] + '\n')
            print(row)
            writer.writerow(row)

    shutil.move(tempFile.name, fileMailPassword)
    createCMD.close()


