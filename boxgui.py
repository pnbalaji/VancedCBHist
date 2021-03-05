from pymsgbox import confirm, password, prompt, alert
from tkinter import *
from tkinter.filedialog import *
from encryption import password_decrypt
from bs4 import BeautifulSoup
import hashlib
import datetime
import base64
import sqlite3
import webbrowser
import pyperclip
import requests

root = Tk()
root.withdraw()


def valid_input(validator, q, title='Prompt', default=''):
    correct = False
    while not correct:
        ans = pprompt(q, title, default)
        if validator(ans):
            correct = True
            return validator(ans)
        if ans == None:
            quit()


def cconfirm(text, title='Confirmation', buttons=['Cancel', 'OK']):
    ans = confirm(text, title, buttons)
    if not ans or ans.lower() in ['cancel', 'quit', 'exit', 'close', 'no']:
        quit()
    return ans


def pprompt(q, title='Prompt', default=''):
    ans = prompt(q, title, default)
    if not ans:
        quit()
    return ans


def cleanup():
    decur.close()
    deconn.close()
    cur.close()
    conn.close()


def decrypt_db():
    values = get_data()
    all_done = True
    pwd = b''
    for ind, val in enumerate(values):
        if ind == int(config['get_vals']):
            all_done = False
            alert(f'Decrypted {ind} values, aborting.', 'Task finished', 'OK')
            break
        print('\n\n', ind, val, '\n\n')
        done = False
        while hashlib.sha1(pwd).hexdigest() != val[1] and not done:
            alert(
                f'Password stored in memory does not match password of value at index {ind}.', 'There\'s a problem', 'OK')
            pwd_ = password('Please enter the password.',
                            'Password', mask='\u00b7')
            if not pwd_ or not pwd_.strip():
                alert('Skipping value as password was not entered.', 'Warning', 'OK')
                done = True
                break
            pwd = pwd_.encode()
        if done:
            cconfirm('It seems you did not enter the password. Quit the program?', 'Hmm...', [
                     'Continue', 'Quit'])
            continue
        insert_value(val, pwd)
    if all_done:
        alert('Decrypted all values.', 'Task finished', 'OK')


def get_data():
    cur.execute('SELECT * FROM CBDATA ORDER BY COPIED_TIMESTAMP DESC')
    for val in cur.fetchall():
        yield val


def valid_int(ans):
    try:
        return int(ans)
    except:
        return False


def insert_value(val: tuple, pwd: bytes):
    decur.execute('INSERT INTO CBDATA VALUES (?, ?)', (
        password_decrypt(base64.b64decode(
            val[0].encode()), pwd.decode()),
        datetime.datetime.fromtimestamp(
            float(val[2])).strftime('%a %b %m %I:%M:%S %p')
    ))
    deconn.commit()


__version__ = 'v1.0.0'
try:
    resp = requests.get('https://github.com/pnbalaji/VancedCBHist')
    if resp:
        soup = BeautifulSoup(resp.text, 'html.parser')
        el = soup.select_one(
            'span.css-truncate.css-truncate-target.text-bold.mr-2')
        if el.text.strip() != __version__:
            ans = cconfirm(
                'There is an update available. What would you like to do?\n' +
                'NOTE: "Open Update Link" might not work on a few devices.\n\n' + 
                'DETAILS:\n' +
                'Current version: ' + __version__ + '\n' +
                'Available update: ' + el.text.strip(),
                'Update Vanced CB Hist',
                ['Open Update Link', 'Copy Update Link', 'Skip Update']
            )
            if not ans:
                alert('Skipping update.', 'Update Vanced CB Hist')
            elif 'Open' in ans:
                webbrowser.open_new_tab(
                    'https://github.com/pnbalaji/VancedCBHist/releases/tag/' + el.text.strip())
                alert('Opened in new tab.', 'Update Vanced CB Hist')
            elif 'Copy' in ans:
                pyperclip.copy(
                    'https://github.com/pnbalaji/VancedCBHist/releases/tag/' + el.text.strip())
                alert('Update link copied to clipboard.', 'Update Vanced CB Hist')
            elif 'Skip' in ans:
                alert('Skipping update.', 'Update Vanced CB Hist')
except:
    pass

cconfirm('What would you like to do?', 'Vanced CB Hist',
         ['Decrypt a Database', 'Quit'])
config = {}
filename = askopenfilename(
    title='Select a database',
    filetypes=(
        ('database files', '*.db'),
        ('sqlite3 files', '*.sqlite3')
    )
)

if not filename:
    quit()

config['db'] = filename
conn = sqlite3.connect(filename)
cur = conn.cursor()
writedb = asksaveasfilename(
    title='Output database',
    filetypes=(
        ('database files', '*.db'),
        ('sqlite3 files', '*.sqlite3')
    )
)
if not writedb:
    quit()
if writedb.endswith('.sqlite3.db'):
    writedb = writedb[:-11] + '.sqlite3'
config['decrypt_db_fname'] = writedb
deconn = sqlite3.connect(writedb)
decur = deconn.cursor()
decur.execute('DROP TABLE IF EXISTS CBDATA')
decur.execute('''\
CREATE TABLE CBDATA(
    DECRYPTED TEXT,
    TIME_COPIED TEXT
)\
''')
deconn.commit()
config['get_vals'] = valid_input(
    valid_int,
    'How many values would you like to decrypt (from the top of the database) [-1=all]?',
    'Decrypt database'
)
ans_ = cconfirm('Start decrypting?', 'Decrypt a database', ['Yes', 'No'])
decrypt_db()
cleanup()
