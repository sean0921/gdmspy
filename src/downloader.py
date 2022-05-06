#!/usr/bin/env python3

# Output URLs should be like:
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN&datev=1991-03-12%2006:04:06
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/cwb24/Event/2017/02/&file=14101712.P17&sys=CWB24

from typing import Tuple
from zenipy.zenipy import entry, zlist, password
import pycurl_requests as requests
import urllib.parse
from pathlib import Path
from send2trash import send2trash
import magic
import re

default_user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
baseurl='https://gdms.cwb.gov.tw/'
cwb_urltype = {'CWBSN': 'download.php?dest_path=//gdms-file1/GDMS/s13/Event', 'CWB24': 'download.php?dest_path=//gdms-file1/GDMS/cwb24/Event'}

def fetch_the_cookie(url) -> str:
    # fetch the cookie
    with requests.Session() as session:
        pre_response = session.get(url)
        if pre_response.status_code != 200:
            print(f'{pre_response.status_code}!')
            exit(1)
        session_cookie = pre_response.headers['Set-Cookie']
    return(session_cookie)

########################## Zenipy config

def gen_user_config() -> Tuple[str, str, str, str, str]:
    default_list_filename = 'request_list.txt'
    default_output_dir = 'output'
    gdms_id = entry(
        text='Please Enter Your GDMS ID',
        placeholder=f'yourid',
        title='GDMS ID',
        width=330, height=120, timeout=None
    )
    gdms_passwd = password(
        text='Please Enter Your GDMS Password',
        placeholder=f'yourid',
        title='GDMS Password',
        width=330, height=120, timeout=None
    )
    seis_network_info = zlist(
        ['CWB Seis Network'],
        ['CWB24','CWBSN'],
        print_columns=None,
        text='Please Select Your CWB Network',
        title='SeisNetwork',
        width=400, height=200, timeout=None
    )
    list_filename = entry(
        text='Please Enter List Filename',
        placeholder=f'{default_list_filename}',
        title='Pfile List',
        width=330, height=120, timeout=None
    )
    output_dir = entry(
        text='Please Enter Output Directory',
        placeholder=f'{default_output_dir}',
        title='Output Dir',
        width=330, height=120, timeout=None
    )
    if None in (gdms_id, gdms_passwd, seis_network_info, list_filename, output_dir):
        print('Incomplete inputs.  Abort!')
        exit(1)

    gdms_id = urllib.parse.quote(gdms_id, safe='')
    gdms_passwd = urllib.parse.quote(gdms_passwd, safe='')
    seis_network = seis_network_info[0]


    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return(gdms_id, gdms_passwd, seis_network, list_filename, output_dir)

######################### Login and activate session and cookies

def main():
    gdms_id, gdms_passwd, seis_network, list_filename, output_dir = gen_user_config()
    download_baseurl = cwb_urltype[f'{seis_network}']
    ses_cookie = fetch_the_cookie(baseurl)
    user_agent = default_user_agent

    post_result = requests.post(
        f'{baseurl}/login/member_login.php',
        data = f'account={gdms_id}&pass={gdms_passwd}&x=0&y=0',
        headers = {
            'User-Agent': f'User-Agent: {default_user_agent}',
            'Cookie': f'{ses_cookie}',
            'Referer': f'{baseurl}/index.php',
            'Sec-Fetch-Site': 'same-origin',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    ################## Download files

    if post_result.status_code != 200:
        print(f'{post_result.status_code}!')
        exit(1)
    else:
        headers = {'User-Agent': f'User-Agent: {user_agent}', 'Cookie': f'{ses_cookie}'}
        f=open(f'{list_filename}')
        lines=f.readlines()
        f.close()

    for i in lines:
        request_filename=i[0:12]
        pfile=request_filename
        year=( 19 + int( int(pfile[0:2]) / 12 ) )*100 + int(pfile[10:12])
        month=int(pfile[0:2])%12
        day=int(pfile[2:4])
        url=f'{baseurl}{download_baseurl}/{year}/{month:02d}/&file={pfile:12s}&sys={seis_network}'
        print(f'Download URL: {url}')
        r=requests.get(f'{url}', headers=headers)
        if r.status_code != 200:
            print(f'{post_result.status_code}!')
            exit(1)
        else:
            downloaded_filepath = f'{output_dir}/{request_filename}'
            with open(f'{downloaded_filepath}','w') as c:
                c.write(r.text)
            download_filetype = magic.from_file(f'{downloaded_filepath}')
            if re.match('^HTML document', download_filetype):
                print(f'Downloaded file may broken! ({request_filename})')
                send2trash(downloaded_filepath)
                print(f'Moved {request_filename} to Recycle Bin!')
                continue
            print(f'{request_filename} downloaded!')

if __name__ == '__main__':
    main()
