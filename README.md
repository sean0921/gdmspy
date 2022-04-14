# GDM*Spy*: the Old-GDMS P-file Downloader

## Requirement
- python3 (3.9)
- gtk3 (PyGObject 3.42.0)
- zenipy (0.1.5)
- requests (2.25.1)
- urllib3 (1.26.5)

## Usage
```bash
python3 downloader.py
```

## post processing
```bash
dos2unix *
sed -i 's/ \./0\./g' ????????.???  
sed -i 's/ -\./-0\./g' ????????.???                      
```

## Demo
- ![](pics/01_enter_id.png)
- ![](pics/02_enter_passwd.png)
- ![](pics/03_select_network.png)
- ![](pics/04_1_select_list.png)
- ![](pics/04_2_list_format.png)
- ![](pics/05_set_output_dir.png)
- ![](pics/06_downloading.png)

## Known Problems
Because GDMS website will still response HTTP 200 when Pfile search error occurs.  Please manually check your downloaded P-file format is correct by `file ????????.???` (in Unix-like system)
