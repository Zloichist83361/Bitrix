import ftputil
import warnings
import logging

logger = logging.getLogger('TAKE_FTP')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('mylog.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

warnings.filterwarnings('ignore')

host ='185.63.60.36'
username ='anonymous'
password =''
port = '8888'

try:
    ftp_host = ftputil.FTPHost(host, username, password, port)
    logger.debug(f'Connect to FTP {host} ')
    ftp_host.use_list_a_option = False
    with ftp_host:
        list = ftp_host.listdir(ftp_host.curdir)
        logger.debug(f'Get file list {list}')
        for fname in list:
            if not ('100-0319.zip') in fname:
                logger.error('Not file')
            else:
                fname = '100-0139.zip'
                logger.debug(f'File download {fname}')
                ftp_host.download(fname, 'ftp/' + fname)
                logger.info(f'Download successfully {fname}')
except Exception:
    logging.error('Error server')
    raise



