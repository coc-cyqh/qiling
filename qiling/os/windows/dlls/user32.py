#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org) 

import struct
from qiling.os.windows.fncc import *
from qiling.os.windows.utils import *


# INT_PTR DialogBoxParamA(
#   HINSTANCE hInstance,
#   LPCSTR    lpTemplateName,
#   HWND      hWndParent,
#   DLGPROC   lpDialogFunc,
#   LPARAM    dwInitParam
# );
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "hInstance": HANDLE,
    "lpTemplateName": POINTER,
    "hWndParent": HANDLE,
    "lpDialogFunc": POINTER,
    "dwInitParam": POINTER
})
def hook_DialogBoxParamA(ql, address, params):
    ret = 0
    return ret


# UINT GetDlgItemTextA(
# 	HWND  hDlg,
# 	int   nIDDlgItem,
# 	LPSTR lpString,
# 	int   cchMax
# );
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "hDlg": HANDLE,
    "nIDDlgItem": INT,
    "lpString": POINTER,
    "cchMax": INT
})
def hook_GetDlgItemTextA(ql, address, params):
    ret = 0
    hDlg = params["hDlg"]
    nIDDlgItem = params["nIDDlgItem"]
    lpString = params["lpString"]
    cchMax = params["cchMax"]

    ql.stdout.write(b"Input DlgItemText :\n")
    string = ql.stdin.readline().strip()[:cchMax]
    ret = len(string)
    ql.uc.mem_write(lpString, string)

    return ret


# int MessageBoxA(
#     HWND   hWnd,
#     LPCSTR lpText,
#     LPCSTR lpCaption,
#     UINT   uType
#     );
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "hWnd": HANDLE,
    "lpText": STRING,
    "lpCaption": STRING,
    "uType": UINT
})
def hook_MessageBoxA(ql, address, params):
    ret = 2
    return ret


# BOOL EndDialog(
#   HWND    hDlg,
#   INT_PTR nResult
# );
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "hDlg": HANDLE,
    "nResult": POINTER
})
def hook_EndDialog(ql, address, params):
    ret = 1
    return ret


# HWND GetDesktopWindow((
# );
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={})
def hook_GetDesktopWindow(ql, address, params):
    pass

#BOOL OpenClipboard(
#  HWND hWndNewOwner
#);
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "hWndNewOwner": HANDLE
})
def hook_OpenClipboard(ql, address, params):
    return ql.clipboard.open(params['hWndNewOwner'])

#BOOL CloseClipboard();
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={})
def hook_CloseClipboard(ql, address, params):
    return ql.clipboard.close()

#HANDLE SetClipboardData(
#  UINT   uFormat,
#  HANDLE hMem
#);
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "uFormat": UINT,
    "hMem": HANDLE
})
def hook_SetClipboardData(ql, address, params):
    return ql.clipboard.set_data(params['uFormat'], params['hMem'])

#HANDLE GetClipboardData(
#  UINT uFormat
#);
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "uFormat": UINT
})
def hook_GetClipboardData(ql, address, params):
    data = ql.clipboard.get_data(params['uFormat'])
    addr = ql.heap.mem_alloc(len(data))
    ql.uc.mem_write(addr, data)
    return addr

#BOOL IsClipboardFormatAvailable(
#  UINT format
#);
@winapi(x86=X86_STDCALL, x8664=X8664_FASTCALL, params={
    "uFormat": UINT
})
def hook_IsClipboardFormatAvailable(ql, address, params):
    rtn = ql.clipboard.format_available(params['uFormat'])
    return rtn
