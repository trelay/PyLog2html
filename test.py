#!/usr/bin/python3
from htmllog import *
log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

logger = PyLogger(filename='test_log.html', html_format=log_format,
		mode='a', title='Test_Title', level=10, console_log=True)
xxx='ddddddd'

for i in range(10):
	logger.debug('This is debug')
	logger.info('This is info')
	logger.warning("This is <hl>warning</hl>")
	logger.error('This is <hl>error</hl>'+xxx)
	logger.info('_____________')
