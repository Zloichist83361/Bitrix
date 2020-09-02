import ftputil
import warnings
import logging
import sentry_sdk
import time

sentry_sdk.init("https://9bb20182388f4a05a93b80a15c333130@o419540.ingest.sentry.io/5334036")

logger = logging.getLogger('TAKE_FTP')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('my_log.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

warnings.filterwarnings('ignore')

host = '109.68.214.235'
username = 'ikea'
password = 'Gb23qJ0s1'
port = '21'


def get_last_file_from_ftp():
    try:
        ftp_host = ftputil.FTPHost(host, username, password, port)
        logger.debug(f'Connect to FTP {host}')
        ftp_host.use_list_a_option = False
        with ftp_host:
            list = ftp_host.listdir(ftp_host.curdir)
            list_file = ''
            for filename in list:
                list_file += '\t\t' + filename + '\n'
            logger.debug(f'Get file list \n {list_file}')
            for filename in list:
                if filename[0]:
                    ftp_host.download(filename, 'Ftp_download/' + filename)
                    logger.debug(f'File download {filename}')
                    logger.info(f'Download successfully {filename}')
                    return filename
                else:
                    logger.error('Invalid file')
    except ConnectionError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)


time.sleep(300)
