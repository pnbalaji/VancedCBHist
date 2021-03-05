from encryption import password_encrypt
from nfilepicker import select_folder
from getpass import getpass
from argparse import ArgumentParser
from hashlib import sha1
import sqlite3
import time
import sys
import os.path
import pyperclip
import base64


def cleanup():
    cur.close()
    conn.close()


def start_service():
    global current
    while True:
        try:
            if sha1(pyperclip.paste().encode()).hexdigest() != current:
                current_time = str(time.time())
                insert_entry(pyperclip.paste(), current_time)
                current = sha1(pyperclip.paste().encode()).hexdigest()
                print('inserted new value')
        except KeyboardInterrupt:
            break
        except:
            pass
        time.sleep(0.125)


def insert_entry(cb_data, time_copied):
    values = {1: base64.b64encode(password_encrypt(cb_data.encode(), pwd or 'VancedCBHist')).decode(), 2: sha1(
        (pwd or 'VancedCBHist').encode()).hexdigest(), 3: time_copied}
    cur.execute('INSERT INTO CBDATA VALUES (?, ?, ?)',
                (values[1], values[2], values[3]))
    conn.commit()

parser = ArgumentParser(description='a tool to encrypt and save clipboard history in a database')
parser.add_argument('-p', '--pwd', type=str, help='password to encrypt with')
parser.add_argument('-o', '--output', type=str, help='output database file')
args = parser.parse_args()
if args.pwd:
    pwd = args.pwd
else:
    pwd = getpass('password [default=VancedCBHist]: ')
config = {}
if args.output:
    if not args.output.lower().endswith(('.db', '.sqlite3')):
        sys.exit('please enter a .db or a .sqlite3 file')
    if not os.path.split(args.output)[0]:
        pass
    elif not os.path.isdir(os.path.split(args.output)[0]):
        sys.exit(f'invalid directory: {os.path.split(args.output)[0]}')
    config['db'] = args.output
else:
    input('hit enter to select the folder to put the output database in. ')
    outfolder = select_folder('choose a folder to save the database in. ')
    outfname = input('please enter the filename of the output database: ').rstrip(
        '/').rstrip('\\')
    if not outfname.endswith(('.db', '.sqlite3')):
        outfname += '.db'
    outfname = os.path.split(outfname)[-1]
    config['db'] = os.path.join(outfolder, outfname)
conn = sqlite3.connect(config['db'])
cur = conn.cursor()
current = None

if __name__ == '__main__':
    cur.execute('''\
CREATE TABLE IF NOT EXISTS CBDATA(
    ENCRYPTED_B64 TEXT,
    PWD_SHA1 TEXT,
    COPIED_TIMESTAMP TEXT
)\
''')
    try:
        start_service()
    except KeyboardInterrupt:
        pass

cleanup()
