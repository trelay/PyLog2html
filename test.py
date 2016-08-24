#!/usr/bin/env python3
from PyLog2html import *
logger=PyLogger(html_filename='test.html',console_log=True)

if __name__=="__main__":
	for i in range(6):
		logger.debug('This is debug')
		logger.info('This is info')
		logger.warning("This is <hl>warning</hl>")
		logger.error('This is <hl>error</hl> xxx')
		logger.info('_____________')
