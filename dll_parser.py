import re
import subprocess

def list_dlls():
    f = open('dll_list.txt', 'w')
    text = subprocess.call(['Listdlls.exe', 'notepad.exe'], stdout = f)
    f.close()


def dll_parser():
    file = open("dll_list.txt", 'r')
    malicious_list = []

    for line in file:
        result = re.search('(\w+\.dll)', line)
        if result and not (result.group(1) in original_list()):
            malicious_list.append(result.group(1))

    print(malicious_list)
    file.close()


def original_list():
    return ['ntdll.dll', 'kernel32.dll', 'comdlg32.dll', 'ADVAPI32.dll', 'RPCRT4.dll', 'Secur32.dll', 'COMCTL32.dll', 'msvcrt.dll', 'GDI32.dll', 'USER32.dll', 'SHLWAPI.dll', 'SHELL32.dll', 'WINSPOOL.DRV', 'ShimEng.dll', 'AcGenral.DLL', 'WINMM.dll', 'ole32.dll', 'OLEAUT32.dll', 'MSACM32.dll', 'VERSION.dll', 'USERENV.dll', 'UxTheme.dll']


list_dlls()
dll_parser()
