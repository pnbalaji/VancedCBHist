from encryption import password_decrypt
from getpass import getpass
from argparse import ArgumentParser
from nfilepicker import select_file, select_folder
import sqlite3
import os
import hashlib
import sys
import datetime
import os.path
import base64


def decrypt_db():
    values = get_data()
    all_done = True
    pwd = b''
    for ind, val in enumerate(values):
        if ind == int(config['get_vals']):
            all_done = False
            print('decrypted', ind, 'values, aborting')
            break
        print('\n\n', ind, val, '\n\n')
        done = False
        while hashlib.sha1(pwd).hexdigest() != val[1] and not done:
            print(
                '\n\npassword stored in memory does not match password of value at index', ind, '\n\n')
            try:
                pwd_ = getpass('password [^d (EOF)=skip value]: ')
            except EOFError:
                done = True
                break
            pwd = pwd_.encode()
        if done:
            continue
        insert_value(val, pwd)
    if all_done:
        print('decrypted all values')


def get_data():
    cur.execute('SELECT * FROM CBDATA ORDER BY COPIED_TIMESTAMP DESC')
    for val in cur.fetchall():
        yield val


def insert_value(val: tuple, pwd: bytes):
    decur.execute('INSERT INTO CBDATA VALUES (?, ?)', (
        password_decrypt(base64.b64decode(
            val[0].encode()), pwd.decode()),
        datetime.datetime.fromtimestamp(
            float(val[2])).strftime('%a %b %m %I:%M:%S %p')
    ))
    deconn.commit()


def cleanup():
    decur.close()
    deconn.close()
    cur.close()
    conn.close()

parser = ArgumentParser(description='a tool to decrypt a Vanced CB Hist database')
parser.add_argument('-i', '--input', type=str, help='input database file (encrypted)')
parser.add_argument('-o', '--output', type=str, help='output database file')
parser.add_argument('-g', '--get-vals', type=int, help='the number of values to get from the database [-1=all]')
args = parser.parse_args()
config = {}
if args.input:
    if not os.path.isfile(args.input):
        sys.exit(f'file not found: {args.input}')
    config['db'] = args.input
else:
    input('hit enter to select the encrypted database.')
    config['db'] = select_file('choose a database.', ('.db', '.sqlite3'))
if args.output:
    if not args.output.lower().endswith(('.db', '.sqlite3')):
        sys.exit('please enter a .db or a .sqlite3 file')
    if not os.path.split(args.output)[0]:
        pass
    elif not os.path.isdir(os.path.split(args.output)[0]):
        sys.exit(f'invalid directory: {os.path.split(args.output)[0]}')
    config['decrypt_db_fname'] = args.output
else:
    input('hit enter to select the folder to put the output database in.')
    defolder = select_folder('choose a folder to save the database in.')
    dedbname = input('please enter the filename of the output database: ').rstrip(
        '/').rstrip('\\')
    if not dedbname.endswith(('.db', '.sqlite3')):
        dedbname += '.db'
    dedbname = os.path.split(dedbname)[-1]
    config['decrypt_db_fname'] = os.path.join(defolder, dedbname)
if args.get_vals:
    config['get_vals'] = args.get_vals
else:
    config['get_vals'] = int(
        input('how many values do you want to decrypt from the database [-1=all]: '))
deconn = sqlite3.connect(config['decrypt_db_fname'])
decur = deconn.cursor()
conn = sqlite3.connect(config['db'])
cur = conn.cursor()

if __name__ == '__main__':
    decur.execute('DROP TABLE IF EXISTS CBDATA')
    decur.execute('''\
CREATE TABLE CBDATA(
    DECRYPTED TEXT,
    TIME_COPIED TEXT
)\
''')
    deconn.commit()
    decrypt_db()

cleanup()
