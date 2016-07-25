#!/usr/bin/python3
from PyLog2html import *
try:
	raise ValueError('variable enable by purpose')
	from config import CONF
	app_name=CONF.LOG.app_name
	Keyword_Italic=CONF.LOG.Keyword_Italic
	Keyword_FontSize=CONF.LOG.Keyword_FontSize
	HighLight_msg_tag_start=CONF.LOG.HighLight_msg_tag_start
	HighLight_msg_tag_end=CONF.LOG.HighLight_msg_tag_end
	msg_color=CONF.LOG.color
	log_format=CONF.LOG.log_format
	HtmlmaxBytes=CONF.LOG.HtmlmaxBytes
	console_log=CONF.LOG.console_log
	html_title=CONF.LOG.title
	html_filename=CONF.LOG.logfilename
	Html_Rotating=CONF.LOG.Html_Rotating
	Html_backupCount=CONF.LOG.Html_backupCount
except:
	app_name="Red_Fish"
	Keyword_Italic=True
	Keyword_FontSize=5
	HighLight_msg_tag_start="<hl>"
	HighLight_msg_tag_end="</hl>"
	msg_color=dict(
	err_color="magenta",
	warn_color="orange",
	info_color="white",
	dbg_color="white")
	log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
	HtmlmaxBytes=1024*1024*50
	console_log=True
	html_title="Default Title"
	html_filename="Redfish_log.html"

logger=PyLogger(name=app_name, html_filename=html_filename, mode='a',
    html_title=html_title,level=logging.DEBUG,
    HtmlmaxBytes=HtmlmaxBytes, encoding=None, delay=False,
    html_format=log_format, msg_color=msg_color,
    Keyword_Italic=Keyword_Italic,Keyword_FontSize=Keyword_FontSize,
	HighLight_msg_tag_start=HighLight_msg_tag_start,
    HighLight_msg_tag_end=HighLight_msg_tag_end,console_log=console_log, 
	Html_Rotating=False,Html_backupCount=5)

for i in range(6):
	logger.debug('This is debug')
	logger.info('This is info')
	logger.warning("This is <hl>warning</hl>")
	logger.error('This is <hl>error</hl> xxx')
	logger.info('_____________')
