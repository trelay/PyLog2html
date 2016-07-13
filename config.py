#!/usr/bin/python3
from oslo.config import cfg
import os.path
import re

def find_cfg_file():
	conf_list=['Redfish.conf','../Redfish.conf','../../Redfish.conf']
	for conf_file in conf_list:
		if os.path.isfile(conf_file):
			return conf_file
###############################################################
rest_group = cfg.OptGroup(
	name='REST', 
	title='RESTful group options'
)
rest_cfg_opts = [
	cfg.StrOpt(
		name='client_name',
		default='redfish',
		help='Client app name that communicates with resetful'),

	cfg.IntOpt(
		name='bind_port',
		default=8888,
		help='Port number the server listens on.'),

	cfg.ListOpt(
		name='ver_support',
		default=['1'],
		help='The ver of Redfish this app supports.')
]
###############################################################
main_group = cfg.OptGroup(
	name='MAIN', 
	title='MAIN group options'
)
main_cfg_opts = [
	cfg.StrOpt(
         name='value_file',
         default='/product/url_dict.conf',
         help='Path of comparing file'),
     cfg.IntOpt(
         name='cycle',
         default=2,
         help='cycle to execute.')
]
##########################################################3
log_group = cfg.OptGroup(
	name='LOG', 
	title='LOG group options'
)

log_cfg_opts = [

	cfg.StrOpt(
	name='app_name',
	default='redfish_test',
	help='APP name showed in Log'),

	cfg.StrOpt(
	name='logfilename',
	default='./redfish.log',
	#default=None,
	help='Log file path.'),

	cfg.StrOpt(
	name='log_format',
	default=None,
	help='Log format in log file.'),

	cfg.IntOpt(
	name='root_level',
	default=10,
	help='Log level for global.'),

	cfg.IntOpt(
	name='ch_level',
	default=10,
	help='Log level for console stream.'),

	cfg.IntOpt(
	name='fh_level',
	default=20,
	help='Log level for file stream.'),

	cfg.StrOpt(
	name='html_color',
	default='color_1',
	help='Choose one in LOG_COLOR, color_1 or color_2'),

	cfg.DictOpt(
	name='color',
	default={},
	help='The main color cheme for html log, generally \
		keep it emtpy'),

	cfg.DictOpt(
	name="color_1",
	default={"err_color": "#FF0000",
			"warn_color": "#FFFF00",
			"info_color": "#FFFFFF",
			"dbg_color": "#FFFFFF"},
	help='The html color scheme option1'),

	cfg.DictOpt(
	name="color_2",
	default={"err_color": "#FF0000",
			"warn_color": "#FFA500",
			"info_color": "#FFFFFF",
			"dbg_color": "#FFFFFF"},
	help='The html color scheme option2'),
	
	cfg.BoolOpt(
	name="Keyword_Italic",
	default=True,
	help='Whether the key work need to be italic in html log'),

	cfg.IntOpt(
	name='Keyword_FontSize',
	default=5,
	help='How is the font size for keyword in html log.'),

	cfg.StrOpt(
	name='HighLight_msg_tag_start',
	default='<hl>',
	help='start tag to mark the keyword to be it'),

	cfg.StrOpt(
	name='HighLight_msg_tag_end',
	default='</hl>',
	help='end tag to mark the keyword to be it'),
	
	cfg.StrOpt(
	name='title',
	default='default_title',
	help='The title of the html log file'),

	cfg.IntOpt(
	name='HtmlmaxBytes',
	default=50*1024*1024,
	help='The size of the html file, keep it small\
		otherwise, it takes long time to open it in brower'),

	cfg.BoolOpt(
	name="console_log",
	default=False,
	help='Whether to print log to console'),

	cfg.BoolOpt(
	name="Html_Rotating",
	default=True,
	help='Whether to rotate the log file if it over the HtmlmaxBytes'),

	cfg.IntOpt(
	name='Html_backupCount',
	default=5,
	help='If the "Html_Rotating" is open, \
		Count of html file will be used to backup'),

]
##########################################################3
request_group = cfg.OptGroup(
	name='REQUEST',
	title='Request options'
)
req_fail_opts = [
	cfg.FloatOpt(
	name='http_time',
	default= 0.4,
	help='The limit of request time'),

	cfg.FloatOpt(
	name='timeout',
	default= 2.0,
	help='Timeout to request an URL'),

	cfg.IntOpt(
	name='retries',
	default= 8,
	help='How many times will retry after failure'),

	cfg.FloatOpt(
	name='delay',
	default= 1.5,
	help='How long will execute the next retry'),

	cfg.IntOpt(
	name='backoff',
	default= 2,
	help='backoff times will retry'),

	cfg.BoolOpt(
	name='failonerror',
	default=False,
	help="whether we need stop if occor error")
]
##########################################################3
cli_group=cfg.OptGroup(
	name="CLI",
	title = 'Cli options'
)

cli_opts = [
	cfg.IntOpt(
		name='retry',
		positional=False,
    	help='How many times retryies after failure'),
	cfg.StrOpt(
		name='logname',
		positional=False,
    	help='Location for the execution log'),
	cfg.StrOpt(
		name='comp_file',
		positional=False,
    	help='The url response data compare file'),
	cfg.IntOpt(
		name='cycles',
		positional=False,
    	help='How many times we scan the nodes'),
	cfg.StrOpt(
		name='time_to_stop',
		positional=False,
    	help='The datetime we stop testing.\
        Format: 2016-06-21 12:00:59')

]

CONF = cfg.CONF
CONF.register_group(rest_group)
CONF.register_opts(rest_cfg_opts, rest_group)

CONF.register_group(main_group)
CONF.register_opts(main_cfg_opts, main_group)

CONF.register_group(log_group)
CONF.register_opts(log_cfg_opts, log_group)

CONF.register_group(request_group)
CONF.register_opts(req_fail_opts, request_group)

CONF.register_group(cli_group)
CONF.register_cli_opts(cli_opts, cli_group)
CONF(default_config_files=[find_cfg_file()])

#This following condition is to: find the proper color 
#which defines in CONF.LOG.color
if CONF.LOG.html_color=='color_1':
	#Don't use shallow copying here
	CONF.LOG.color.update(CONF.LOG.color_1)
elif CONF.LOG.html_color=='color_2':
	CONF.LOG.color.update(CONF.LOG.color_2)

#This following condition is to: keep the user typed are working.
if CONF.CLI.retry:
	CONF.REQUEST.retries= CONF.CLI.retry
if CONF.CLI.logname:
	CONF.LOG.logfilename= CONF.CLI.logname
else:
	#Locate the axactly postion for redfish.log
	CONF.LOG.logfilename=os.path.join(os.path.dirname(\
		os.path.abspath(__file__)),'..',CONF.LOG.logfilename)
if CONF.CLI.comp_file:
	CONF.MAIN.value_file= CONF.CLI.comp_file
if CONF.CLI.cycles:
	CONF.MAIN.cycle= CONF.CLI.cycles
if CONF.CLI.time_to_stop:
	if not re.search(r'(20\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)', \
				CONF.CLI.time_to_stop):
		msg="The date time you entered is not in the corrent format, as: 2014-12-12 08:30:59"
		raise ValueError(msg) 


if __name__ =="__main__":
	print('CONF.value_file',CONF.MAIN.value_file)
	print('CONF.MAIN.cycle',CONF.MAIN.cycle)
	print('CONF.client_name:',CONF.REST.client_name)
	print('CONF.bind_port:',CONF.REST.bind_port)
	print('CONF.ver_support:',CONF.REST.ver_support)
	print('CONF.LOG.app_name:',CONF.LOG.app_name)
	print('CONF.LOG.logfilename:',CONF.LOG.logfilename)
	print('CONF.LOG.log_format:',CONF.LOG.log_format)
	print('CONF.LOG.root_level:',CONF.LOG.root_level)
	print('CONF.LOG.ch_level:',CONF.LOG.ch_level)
	print('CONF.LOG.fh_level:',CONF.LOG.fh_level)
	print('CONF.REQUEST.http_time:',CONF.REQUEST.http_time)
	print('CONF.REQUEST.retries:',CONF.REQUEST.retries)
	print('CONF.REQUEST.delay:',CONF.REQUEST.delay)
	print('CONF.REQUEST.backoff:',CONF.REQUEST.backoff)
	print('CONF.REQUEST.failonerror:',CONF.REQUEST.failonerror)
	print('CONF.CLI.time_to_stop:',CONF.CLI.time_to_stop)
	print("""CONF.LOG.color:""",CONF.LOG.color)
