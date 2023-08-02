from datetime import datetime,timedelta
import os
from os import path,makedirs

today = datetime.now()
yest = today - timedelta(1)
tgl = yest.strftime('%Y%m%d')
date = yest.strftime('%Y-%m-%d')
f_thn = yest.strftime('%Y')
f_bln = yest.strftime('%-m')
dest_folder = f_thn+'/'+f_bln

des = '/root/sigempa_v2/sipetir/fungsi/data/DB3'+'/'+dest_folder
if path.exists(des):
    print('folder '+des+' ready!')
else:
    os.system('mkdir '+des)
    print('folder created!')

os.system('cp -r /home/ftpternate/ftp/DB3/'+tgl+'.db3 '+des)