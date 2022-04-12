#!/usr/bin/env python3

from zenipy.zenipy import entry, zlist
## TODO: use pycurl
import requests

## TODO: make input
def_cookie='PHPSESSID=54c29e8976cd2c8ebc435bcbc29943e8; lang=tw; TS01d26e96=0107dddfef06b850d868747c7b516541945b9115d469082c34841781c36e50d7950a4b10761d89d768898e9203622a7cdc989faf64'
def_list_filename = 'request_list.txt'
def_user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
def_output_dir = 'output'

baseurl_format_1 = '?dest_path=//gdms-file1/GDMS/s13/Event'
baseurl_format_2 = '?dest_path=//gdms-file1/GDMS/cwb24/Event'

cookie = entry(
    text='Please Enter Your Cookie',
    placeholder=f'{def_cookie}',
    title='Cookie',
    width=330, height=120, timeout=None
)  
download_baseurl = zlist(
    ['CWB URL Type'],
    ['?dest_path=//gdms-file1/GDMS/cwb24/Event','?dest_path=//gdms-file1/GDMS/s13/Event'],
    print_columns=None,
    text='Please Select Your Baseurl',
    title='Baseurl',
    width=400, height=200, timeout=None
)[0]
list_filename = entry(
    text='Please Enter List Filname',
    placeholder=f'{def_list_filename}',
    title='Pfile List',
    width=330, height=120, timeout=None
)
user_agent = entry(
    text='Please Enter Your User Agent',
    placeholder=f'{def_user_agent}',
    title='User Agent',
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
output_dir = entry(
    text='Please Enter Output Directory',
    placeholder=f'{def_output_dir}',
    title='Output Dir',
    width=330, height=120, timeout=None
)

if None in (cookie, download_baseurl, list_filename, user_agent, seis_network, output_dir):
    print('Incomplete inputs.  Abort!')
    exit(1)

baseurl='https://gdms.cwb.gov.tw/download.php'
headers = {'User-Agent': f'User-Agent: {user_agent}', 'Cookie': f'{cookie}'}

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
    r=requests.get(f'{url}', headers=headers)
    if r.ok:
        ## TODO: make input
        with open(f'{output_dir}/{request_filename}','w') as c:
            c.write(r.text)
        print(f'Downloaded {request_filename}!')

# Output URLs should be like:
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN&datev=1991-03-12%2006:04:06
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/s13/Event/1991/03/&file=03120603.P91&sys=CWBSN
#     https://gdms.cwb.gov.tw/download.php?dest_path=//gdms-file1/GDMS/cwb24/Event/2017/02/&file=14101712.P17&sys=CWB24
  
