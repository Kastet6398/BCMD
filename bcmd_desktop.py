import subprocess
import webbrowser
from rich.console import Console
import urllib.request
import platform
import socket
import re
import uuid
import psutil
import os
import random


class FormatError(Exception):
    pass


class FolderExistsError(Exception):
    pass


console = Console()

prompt = ''
while 1:
    try:
        prompt = console.input('[green]Enter a command: ')
        console.log()

        if prompt.strip().find('#evalute') == 0:
            try:
                if prompt.strip() != '#evalute':
                    console.print('[blue]Processing...')
                    ev = eval(prompt[prompt.find('#evalute') + 9:])
                    console.print(ev)

                else:
                    raise FormatError(
                        'uncorrect format. Must be: #evalute SOME_CODE')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#exit' or prompt.strip() == '#quit':
            break

        elif prompt.strip() == '#vars':
            console.log(log_locals=1)

        elif prompt.strip().find('#password') == 0:
            try:
                num = int(prompt.strip().replace('#password', ''), base=0) if (
                    prompt.strip() != '#password') else 30
                print(''.join([random.choice(list(
                    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')) for _ in range(num)]))
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip().find('#url') == 0:
            try:
                if prompt.strip() != '#url':
                    webbrowser.open_new_tab(prompt.replace('#url ', '', 1))
                else:
                    raise FormatError(
                        'uncorrect format. Must be: #url SOME_URL')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip().find('#source') == 0:
            try:
                if prompt.strip() != '#source':
                    console.print(urllib.request.urlopen(
                        prompt[prompt.find('#source') + 7:]).read().decode())
                else:
                    raise FormatError(
                        'uncorrect format. Must be: #source SOME_URL')
            except:
                console.print_exception(max_frames=10)

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
                        'uncorrect format. Must be: [blue]#write "SOME TEXT" to "FILE PATH"')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip().find('#createfile') == 0:
            try:
                path = prompt[prompt.find('#createfile') + 12:]

                if prompt.strip() != '#createfile':
                    if not os.path.exists(path):
                        open(path, 'a')
                    else:
                        raise FileExistsError(f'file "{path}" already exists.')
                else:
                    raise FormatError(
                        'uncorrect format. Must be: #createfile FILE NAME')
            except:
                console.print_exception(max_frames=10)

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
                        'uncorrect format. Must be: #createfoler FOLDER NAME')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip().find('#delete') == 0:
            try:
                path = prompt[prompt.find('#delete') + 8:]
                if prompt.strip() != '#delete':
                    os.unlink(path)
                else:
                    raise FormatError(
                        'uncorrect format. Must be: #delete PATH')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#clear' or prompt == '\f':
            os.system('cls' if os.name == 'nt' else 'clear')

        elif prompt.strip() == '#help' or prompt.strip() == '?':
            console.rule('ALL COMMANDS')
            console.rule('#evalute')
            console.print(
                'Use [blue]#evalute COMMAND[/blue] to evalute something, \
where COMMAND is Python some code or a mathimatical expression.\n')
            console.rule('#exit')
            console.print(
                'Use [blue]#exit[/blue] or [blue]#quit[/blue] or [blue]Control+z and Enter[/blue] \
or [blue]Control+c[/blue] (not selecting text) to exit console.\n')
            console.rule('#password')
            console.print(
                'Use [blue]#password PASSWORD_LENGTH[/blue] or [blue]#password[/blue] to get the random password, \
where PASSWORD_LENGTH is the length of the password. PASSWORD_LENGTH defaults to 30 if isn\t given.\n')
            console.rule('#url')
            console.print(
                'Use [blue]#url A_URL[/blue] to open the url in new tab in your browser, \
where A_URL is the url you want to open.\n')
            console.rule('#source')
            console.print(
                'Use [blue]#source A_URL[/blue] to get the source of site, \
where A_URL is the site\'s url.\n')
            console.rule('#write')
            console.print(
                'Use [blue]#write "SOME TEXT" to "FILE PATH"[/blue] to write text to file, \
where SOME TEXT is the text and FILE PATH is the path of the file.\n')
            console.rule('#createfile')
            console.print(
                'Use [blue]#createfile FILE PATH[/blue] to create a file, \
where FILE PATH is the path of the file.\n')
            console.rule('#createfolder')
            console.print(
                'Use [blue]#createfolder FOLDER PATH[/blue] to create a folder, \
where FOLDER PATH is the path of the folder.\n')
            console.rule('#delete')
            console.print(
                'Use [blue]#delete PATH[/blue] to delete an object, \
where PATH is the path of the object which will be deleted.\n')
            console.rule('#clear')
            console.print(
                'Use [blue]#clear[/blue] or [blue]CTRL+L and ENTER[/blue] to clear the console.\n')
            console.rule('#help')
            console.print(
                'Use [blue]#help[/blue] or [blue]?[/blue] to view the help.\n')
            console.rule('#sysinfo')
            console.print(
                'Use [blue]#sysinfo[/blue] to view the information of your OS and device.\n')
            console.rule('#platform')
            console.print(
                'Use [blue]#platform[/blue] to view the platform of your device.\n')
            console.rule('#release')
            console.print(
                'Use [blue]#release[/blue] to view the release of your OS.\n')
            console.rule('#version')
            console.print(
                'Use [blue]#version[/blue] to view the full version of your OS.\n')
            console.rule('#architecture')
            console.print(
                'Use [blue]#architecture[/blue] to view the architecture of your device.\n')
            console.rule('#host')
            console.print(
                'Use [blue]#host[/blue] to view the host of your device.\n')
            console.rule('#ip')
            console.print(
                'Use [blue]#ip[/blue] to view your IP address.\n')
            console.rule('#mac')
            console.print(
                'Use [blue]#mac[/blue] to view your MAC addres.\n')
            console.rule('#processor')
            console.print(
                'Use [blue]#processor[/blue] to view the information of processor of your device.\n')
            console.rule('#ram')
            console.print(
                'Use [blue]#ram[/blue] to view free RAM.\n')
            console.rule()
            console.print(
                'You can also use another CMD commands like in your OS\'s command line \
(Windows PowerShell, etc.).\n')

        elif prompt.strip() == '#sysinfo':
            try:
                console.print(f'''Platform: {platform.system()}
Release: {platform.release()}
Version: {platform.version()}
Architecture: {platform.machine()}
Host: {socket.gethostname()}
IP: {socket.gethostbyname(socket.gethostname())}
MAC: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
Processor: {platform.processor()}
RAM: free {round(psutil.virtual_memory().free / (1024.0 ** 3), 3)} GB \
({round(100 - psutil.virtual_memory().percent, 3)}%)''')
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#platform':
            try:
                console.print('Platform: ' + platform.system())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#release':
            try:
                console.print('Release: ' + platform.release())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#version':
            try:
                console.print('Version: ' + platform.version())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#architecture':
            try:
                console.print('Architecture: ' + platform.machine())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#host':
            try:
                console.print('Host: ' + socket.gethostname())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#ip':
            try:
                console.print(
                    'IP: ' + socket.gethostbyname(socket.gethostname()))
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#mac':
            try:
                console.print(
                    'MAC: ' + ':'.join(re.findall('..', '%012x' % uuid.getnode())))
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#processor':
            try:
                console.print('Processor: ' + platform.processor())
            except:
                console.print_exception(max_frames=10)

        elif prompt.strip() == '#ram':
            try:
                console.print(
                    f'RAM: free {round(psutil.virtual_memory().free / (1024.0 ** 3), 3)} GB')
            except:
                console.print_exception(max_frames=10)

        else:
            subprocess.call(prompt, shell=1)
    except:
        break
