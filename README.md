# Vanced CB Hist

A clipboard history program built 100% with Python.

## Getting Started

To run this program, it is recommended to use a `tmux` session.
If you cannot use `tmux`, it's okay. You can run Vanced CB Hist
in the background by adding the `&` suffix.

### Running with Tmux

```sh
me@my-MBP ~ $ tmux
```

This will start a Tmux session.

<details>
<summary>View Output</summary>

```
me@my-MBP ~ $ █










[0] 0:zsh\* "my-MBP" 12:25 03-Mar-21
```

</details>

In the Tmux session, `cd` into the project directory (cloned from GitHub).

```sh
me@my-MBP ~ $ cd /path/to/VancedCBHist/
```

If you want, create a virtual environment.

```sh
me@my-MBP …Hist $ python3 -m pip install -U virtualenv # optional
me@my-MBP …Hist $ virtualenv venv # optional
me@my-MBP …Hist $ source ./venv/bin/activate # unix, optional
me@my-MBP …Hist $ .\venv\Scripts\activate # windows, optional
```

Now, install the requirements.

```sh
(venv) me@my-MBP …Hist $ python3 -m pip install -r requirements.txt
(venv) me@my-MBP …Hist $ python3 -m pip install -U windows-curses # windows, required
```

Now you can run `cbhist.py`.

<details>
<summary>Method 1</summary>
cbhist.py can be used as a CLI.

```sh
(venv) me@my-MBP …Hist $ python3 cbhist.py -p <password> -o <output_db>.<db|sqlite3>
```

</details>

<details>
<summary>Method 2</summary>
You can also run cbhist.py and fill out the information.

```sh
(venv) me@my-MBP …Hist $ python3 cbhist.py
password [default=VancedCBHist]:
hit enter to select the folder to put the output database in.
please enter the filename of the output database: clipboard.db
```

</details>

When `cbhist.py` has started running, you can detach from the shell
session by pressing <kbd>CTRL</kbd> + <kbd>B</kbd> to enter _command mode_,
and then <kbd>D</kbd>.

### Running in a Standard Shell Session

`cd` into the project directory.

```sh
me@my-MBP ~ $ cd /path/to/VancedCBHist/
```

Now you should be inside the cloned project directory.
If you want, create a virtual environment.

```sh
me@my-MBP …Hist $ python3 -m pip install virtualenv # optional
me@my-MBP …Hist $ virtualenv venv # optional
me@my-MBP …Hist $ source ./venv/bin/activate # unix, optional
me@my-MBP …Hist $ .\venv\Scripts\activate # windows, optional
```

Now, install the requirements.

```sh
(venv) me@my-MBP …Hist $ python3 -m pip install -r requirements.txt
(venv) me@my-MBP …Hist $ python3 -m pip install -U windows-curses # windows, required
```

You are ready to run `cbhist.py` now.

```sh
(venv) me@my-MBP …Hist $ python3 cbhist.py -p <password> -o <output_db>.<db|sqlite3> &
```

This should start running `cbhist.py` in the background. Now you can exit the terminal.

```sh
(venv) me@my-MBP …Hist $ exit
```

## Using the GUI Application

`boxgui.py` (the `box` in `boxgui.py` stands for `pymsgbox`,
as the GUI was developed with `pymsgbox`) is a GUI version of
`decrypt_db.py`. This program checks for updates, so it is
recommended to run this file once in a while. To decrypt a
database with `boxgui.py`, follow the steps below.

```sh
(venv) me@my-MBP …Hist $ python3 boxgui.py
```

This command should launch something like this.

[![gui-start-screen.png](https://i.postimg.cc/fLx1VytL/gui-start-screen.png)](https://postimg.cc/hzt2wS0W)

If you see something like this instead, go ahead and update Vanced CB Hist.

[![gui-update-screen.png](https://i.postimg.cc/jdMpSqsP/gui-update-screen.png)](https://postimg.cc/rKtnhkRw)

Once you click "Decrypt a Database", you will be prompted to open an encrypted
database file. Now, select a database.

[![gui-select-in.png](https://i.postimg.cc/dtL3yc6F/gui-select-in.png)](https://postimg.cc/zVY8sM42)

Once you select the input database file, you will be prompted to select the output
one. Select where to save the output database and continue to the next step.

[![gui-select-out.png](https://i.postimg.cc/t4nzDfqQ/gui-select-out.png)](https://postimg.cc/5X1v2sQn)

Now you will see this screen. If you have a really big database and you want to get
a string you copied yesterday, you don't have to wait for hours to decrypt the whole
database. You can enter something like 30 or 50 here to get the last 30 or 50 values
added to the database. If you want to decrypt all the values from the selected database,
enter -1 and continue. If you want to decrypt the last `n` values, enter the number `n`
and continue.

[![gui-get-vals-screen.png](https://i.postimg.cc/G25ckmc3/gui-get-vals-screen.png)](https://postimg.cc/phKbvxh3)

When you see this screen, select "Yes" to start decrypting the database.

[![gui-start-decrypting.png](https://i.postimg.cc/c4qvjFSx/gui-start-decrypting.png)](https://postimg.cc/qgLB6XqS)

If you see this screen, it means the password stored in the program does not
match the password of the value in the database. At first, the password is
set to an empty string. Click "OK" and continue.

[![gui-pwd-input.png](https://i.postimg.cc/DfGZq1bt/gui-pwd-input.png)](https://postimg.cc/kDnqC6sc)

Now you have to enter the password. Enter it and hit the <kbd>Return</kbd>/<kbd>Enter</kbd> key.

[![gui-pwd-input-real.png](https://i.postimg.cc/Y07wNG5H/gui-pwd-input-real.png)](https://postimg.cc/Q9fPhtN4)

Once the values are done decrypting, you will see this screen if you've decrypted
all of the values.

[![gui-all-done.png](https://i.postimg.cc/BvKC3Snn/gui-all-done.png)](https://postimg.cc/XZn5c05R)

If you've decrypted a certain number of values, you will see something like this.

[![gui-n-done.png](https://i.postimg.cc/Wpx5yczd/gui-n-done.png)](https://postimg.cc/F1gbfqjv)

## CLI Usage

### `cbhist.py` Usage

```sh
(venv) me@my-MBP …Hist $ python3 cbhist.py -h
usage: cbhist.py [-h] [-p PWD] [-o OUTPUT]

a tool to encrypt and save clipboard history in a database

optional arguments:
  -h, --help            show this help message and exit
  -p PWD, --pwd PWD     password to encrypt with
  -o OUTPUT, --output OUTPUT
                        output database file

```

### `decrypt_db.py` Usage

```sh
(venv) me@my-MBP …Hist $ python3 decrypt_db.py -h
usage: decrypt_db.py [-h] [-i INPUT] [-o OUTPUT] [-g GET_VALS]

a tool to decrypt a Vanced CB Hist database

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input database file (encrypted)
  -o OUTPUT, --output OUTPUT
                        output database file
  -g GET_VALS, --get-vals GET_VALS
                        the number of values to get from the database [-1=all]

```

## Credits

Developer: [Pranav Balaji Pooruli](mailto:pranav.pooruli@gmail.com)  
Publisher: Balaji Pooruli Neelakantan
