#!/usr/bin/env python3

# Output URLs should be like:
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN&datev=1991-03-12%2006:04:06
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/cwb24/Event/2017/02/&file=14101712.P17&sys=CWB24

from zenipy.zenipy import entry, zlist, password
import requests  ## TODO: use pycurl
import urllib.parse
from pathlib import Path

def_list_filename = 'request_list.txt'
def_user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
def_output_dir = 'output'

baseurl='https://gdms.cwb.gov.tw/'
cwb_urltype = {'CWBSN': 'download.php?dest_path=//gdms-file1/GDMS/s13/Event', 'CWB24': 'download.php?dest_path=//gdms-file1/GDMS/cwb24/Event'}

########################## Zenipy config

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
seis_network = zlist(
    ['CWB Seis Network'],
    ['CWB24','CWBSN'],
    print_columns=None,
    text='Please Select Your CWB Network',
    title='SeisNetwork',
    width=400, height=200, timeout=None
)[0]
list_filename = entry(
    text='Please Enter List Filname',
    placeholder=f'{def_list_filename}',
    title='Pfile List',
    width=330, height=120, timeout=None
)
output_dir = entry(
    text='Please Enter Output Directory',
    placeholder=f'{def_output_dir}',
    title='Output Dir',
    width=330, height=120, timeout=None
)
if None in (gdms_id, gdms_passwd, list_filename, seis_network, output_dir):
    print('Incomplete inputs.  Abort!')
    exit(1)

gdms_id = urllib.parse.quote(gdms_id, safe='')
gdms_passwd = urllib.parse.quote(gdms_passwd, safe='')
download_baseurl = cwb_urltype[f'{seis_network}']
user_agent = def_user_agent

######################### end of Zenipy config

Path(output_dir).mkdir(parents=True, exist_ok=True)

######################### Login and activate session and cookies

session = requests.Session()
response = session.get(baseurl)
if response.status_code == 200:
    ses_cookie_dict = session.cookies.get_dict()
ses_cookie = f'PHPSESSID={ses_cookie_dict["PHPSESSID"]}; lang=tw; TS01d26e96={ses_cookie_dict["TS01d26e96"]}'

post_result = requests.post(
    f'{baseurl}/login/member_login.php',
    data = f'account={gdms_id}&pass={gdms_passwd}&x=0&y=0',
    headers = {
        'User-Agent': f'User-Agent: {def_user_agent}',
        'Cookie': f'{ses_cookie}',
        'Referer': f'{baseurl}/index.php',
        'Sec-Fetch-Site': 'same-origin',
        'Content-Type': 'application/x-www-form-urlencoded'
    } 
)

################## Download files

if post_result.status_code == 200:
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
        print(url)
        r=requests.get(f'{url}', headers=headers)
        if r.status_code == 200:
            ## TODO: make input
            with open(f'{output_dir}/{request_filename}','w') as c:
                c.write(r.text)
            print(f'Downloaded {request_filename}!')
