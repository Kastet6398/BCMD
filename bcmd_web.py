
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import *
import urllib.request
import platform
import socket
import re
import uuid
import psutil
import os
import traceback
import random
import subprocess
import webbrowser
import chardet


class FormatError(Exception):
    pass


class FolderExistsError(Exception):
    pass


def check_valid(text: str):
    if text.strip() == '':
        return 'This field is required.'


@config(theme='dark', description='Main app')
def Main():
    set_env(title='Main app', auto_scroll_bottom=1)

    use_scope('scope1')

    while 1:
        try:
            prompt = textarea('Enter a command: ',
                              placeholder='Write a BCMD command here...',
                              help_text='Write a BCMD command here. Use ? or #help to view help',
                              validate=check_valid)

            if prompt.strip().find('#evalute') == 0:
                try:
                    if prompt.strip() != '#evalute':
                        put_info('⌛ Processing...', closable=1)
                        put_success(
                            eval(prompt[prompt.find('#evalute') + 9:]), closable=1)

                    else:
                        raise FormatError(
                            'incorrect format. Must be: #evalute SOME_CODE')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#exit' or prompt.strip() == '#quit':
                break

            elif prompt.strip() == '#vars':
                put_success(globals(), closable=1)

            elif prompt.strip().find('#password') == 0:
                try:
                    num = int(prompt.strip().replace('#password', ''), base=0) if (
                        prompt.strip() != '#password') else 30
                    put_success(''.join([random.choice(list(
                        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')) for _ in range(num)]),
                        closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#url') == 0:
                try:
                    if prompt.strip() != '#url':
                        webbrowser.open_new_tab(prompt.replace('#url ', '', 1))
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #url SOME_URL')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#source') == 0:
                try:
                    if prompt.strip() != '#source':
                        put_success(urllib.request.urlopen(
                            prompt[prompt.find('#source') + 7:]).read().decode())
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #source SOME_URL')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#write') == 0:
                try:
                    p = prompt.replace('#write', '', 1).split('" to "')

                    if prompt.replace('#write ', '', 1).find('" to "') != -1 \
                            and p[1].strip().endswith('"') and p[0].strip().startswith('"'):

                        f = open(p[1][:p[1].find('"')], 'w')
                        f.write(p[0][p[0].find('"') + 1:])
                        f.close()
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #write "SOME TEXT" to "FILE PATH"')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#createfile') == 0:
                try:
                    path = prompt[prompt.find('#createfile') + 12:]

                    if prompt.strip() != '#createfile':
                        if not os.path.exists(path):
                            open(path, 'a')
                        else:
                            raise FileExistsError(
                                f'file "{path}" already exists.')
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #createfile FILE NAME')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#createfolder') == 0:
                try:
                    path = prompt[prompt.find('#createfolder') + 14:]
                    if prompt.strip() != '#createfolder':
                        if not os.path.exists(path):
                            os.makedirs(path)
                        else:
                            raise FolderExistsError(
                                f'folder "{path}" already exists.')
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #createfoler FOLDER NAME')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip().find('#delete') == 0:
                try:
                    path = prompt[prompt.find('#delete') + 8:]
                    if prompt.strip() != '#delete':
                        os.unlink(path)
                    else:
                        raise FormatError(
                            'incorrect format. Must be: #delete PATH')
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#help' or prompt.strip() == '?':
                put_markdown('''# All commands
## `#evalute`
Use **`#evalute COMMAND`** to evalute something, 
where **`COMMAND`** is some Python code or a mathimatical expression. **Examples:**
- > `#evalute` 5**4
- > `#evalute` exec('variable = "Python"')
## `#exit` 
Use **`#exit`** or **`quit`** to stop the application. 
## `#password`
Use **`#password PASSWORD_LENGTH`** or **`#password`** to get the random password, 
where **`PASSWORD_LENGTH`** is the length of the password. **`PASSWORD_LENGTH`** defaults to 30 if isn't given. **Example:**
> #password 25
## `#url`
Use **`#url SOME_URL`** to open the url in new tab in your browser, 
where **`SOME_URL`** is the url you want to open. **Example:**
> #url www.google.com
## `#source`
Use **`#source AN_URL`** to get the source of site, 
where **`AN_URL`** is the site's url. **Example:**
> #source https://www.google.com
## `#write`
Use **`#write "SOME TEXT" to "FILE PATH"`** to write text to file, 
where **`SOME TEXT`** is the text and **`FILE PATH`** is the path of the file. **Example:**
> #write "Hello, world!" to "helloworld.txt"
## `#createfile`
Use **`#createfile FILE PATH`** to create a file, 
where **`FILE PATH`** is the path of the file. **Example:**
> #createfile hellowrold.txt
## `#createfolder`
Use **`#createfolder FOLDER PATH`** to create a folder, 
where **`FOLDER PATH`** is the path of the folder. **Example:**
> #createfolder my folder
## `#delete`
Use **`#delete PATH`** to delete an object, 
where **`PATH`** is the path of the object which will be deleted. **Example:**
> #delete my folder
## `#clear`
Use **`#clear`** to clear the console.
## `#help`
Use #help or ? to view the help.
## `#sysinfo`
Use **`#sysinfo`** to view the information of your OS and device.
## `#platform`
Use **`#platform`** to view the platform of your device.
## `#release`
Use **`#release`** to view the release of your OS.
## `#version`
Use **`#version`** to view the full version of your OS.
## `#architecture`
Use **`#architecture`** to view the architecture of your device.
## `#host`
Use **`#host`** to view the host of your device.
## `#ip`
Use **`#ip`** to view your IP address.
## `#mac`
Use **`#mac`** to view your MAC addres.
## `#processor`
Use **`#processor`** to view the information of processor of your device.
## `#ram`
Use **`#ram`** to view free RAM.
## Other commands
You can also use another your OS's CMD commands (**`dir`**, **`ls`**, etc.).
# List of commands
- ### `#evalute`
- ### `#exit`
- ### `#password`
- ### `#url`
- ### `#source`
- ### `#write`
- ### `#createfile`
- ### `#createfolder`
- ### `#delete`
- ### `#clear`
- ### `#help`
- ### `#sysinfo`
- ### `#platform`
- ### `#release`
- ### `#version`
- ### `#architecture`
- ### `#host`
- ### `#ip`
- ### `#mac`
- ### `#processor`
- ### `#ram`
- ### OS's CMD commands''')

            elif prompt.strip() == '#sysinfo':
                try:
                    put_info(f'''Platform: {platform.system()}
    Release: {platform.release()}
    Version: {platform.version()}
    Architecture: {platform.machine()}
    Host: {socket.gethostname()}
    IP: {socket.gethostbyname(socket.gethostname())}
    MAC: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
    Processor: {platform.processor()}
    RAM: free {round(psutil.virtual_memory().free / (1024.0 ** 3), 3)} GB \
    ({round(100 - psutil.virtual_memory().percent, 3)}%)''', closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#platform':
                try:
                    put_info('Platform: ' + platform.system(), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#release':
                try:
                    put_info('Release: ' + platform.release(), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#version':
                try:
                    put_info('Version: ' + platform.version(), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#architecture':
                try:
                    put_info('Architecture: ' + platform.machine(), closable=1)
                except:
                    put_error(traceback.format_exc())

            elif prompt.strip() == '#host':
                try:
                    put_info('Host: ' + socket.gethostname(), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#ip':
                try:
                    put_info(
                        'IP: ' + socket.gethostbyname(socket.gethostname()), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#mac':
                try:
                    put_info(
                        'MAC: ' + ':'.join(re.findall('..', '%012x' % uuid.getnode())), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#processor':
                try:
                    put_info('Processor: ' + platform.processor(), closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            elif prompt.strip() == '#ram':
                try:
                    put_info(
                        f'RAM: free {round(psutil.virtual_memory().free / (1024.0 ** 3), 3)} GB \
({round(100 - psutil.virtual_memory().percent, 3)}%)''', closable=1)
                except:
                    put_error(traceback.format_exc(), closable=1)

            else:
                out = subprocess.run(
                    prompt, shell=1, capture_output=1)
                if out.stderr:
                    put_error(out.stderr.decode(chardet.detect(
                        out.stderr)['encoding']), closable=1)
                    continue
                put_success(out.stdout.decode(chardet.detect(
                    out.stdout)['encoding']), closable=1)
        except:
            break


try:
    start_server([Main], 3333, auto_open_webbrowser=1)
except:
    pass
