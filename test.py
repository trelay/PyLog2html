#!/usr/bin/python3
from htmllog import *

logger = HTMLLogger(filename='test_log.html', mode='a', title='Test_Title',version='1.2', level=10)

for i in range(30):
	logger.debug('This is debug')
	logger.info('This is info')
	logger.warning('This is warning')
	logger.error('This is error')
	logger.info('_____________')
