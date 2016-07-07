#!/usr/bin/python3
"""
Python logger rationing to file without limited count.
Usage:
 - call setup and specify the filename, title and level
 - call dbg, info, warn or err to log messages.
"""
import os
import logging
import logging.handlers



#: HTML header (starts the document
START_OF_DOC_FMT = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>%(title)s</title>
<style type="text/css">
body, html {
background: #000000;
width: auto;
font-family: Arial;
font-size: 16px;
color: #C0C0C0;
}
h1 {
color : #FFFFFF;
border-bottom : 1px dotted #888888;
}
.box {
border : 1px dotted #818286;
padding : 5px;
margin: 5px;
width: auto;
background-color : #292929;
}
.err {
word-break:break-all; word-wrap:break-all;
color: %(err_color)s;
font-family : arial;
margin : 0;
}
.warn {
word-break:break-all; word-wrap:break-all;
color: %(warn_color)s;
font-family : arial;
margin : 0;

}
.info {
word-break:break-all; word-wrap:break-all;
color: %(info_color)s;
font-family : arial;
margin : 0;
}
.debug {
word-break:break-all; word-wrap:break-all;
color: %(dbg_color)s;
font-family : arial;
margin : 0;
}
</style>
</head>
<body>
<h1>%(title)s</h1>

<p>Select a category to display:
<select id="mySelect" onchange="myFunction()">
  <option value="ALL">ALL
  <option value="DEBUG">DEBUG
  <option value="INFO">INFO
  <option value="WARNING">WARNING
  <option value="ERROR">ERROR
</select> </p>

<script>
function myFunction() {
var all = document.getElementsByTagName("tr");
var slct_v = document.getElementById("mySelect").value;

for (var i=0, max=all.length; i < max; i++) {
var css_name=all[i].getElementsByTagName("td")[3].getAttribute("class");
	
	if (css_name=="debug" & slct_v=="DEBUG"){
	all[i].style.display='';
	}

	else if (css_name=="info" & slct_v=="INFO"){
	all[i].style.display='';
	}

	else if (css_name=="warn" & slct_v=="WARNING"){
	all[i].style.display='';
	}
	
	else if (css_name=="err" & slct_v=="ERROR"){
	all[i].style.display='';
	}
	
	else{
		if (slct_v=="ALL"){
			all[i].style.display='';
		}
		else{
			all[i].style.display='none';
		};
	};

};
}
</script>

<div class="box">
<table>
"""

END_OF_DOC_FMT = """</table>
</div>
</body>
</html>
"""

MSG_FMT = """
<tr>
<td width="200">%(asctime)s</td>
<td width="100">%(name)s</td>
<td width="100">%(levelname)s</td>
<td class="%(cssname)s">%(message)s</td>
</tr>
"""

MID_OF_DOC_FMT = """
<!--
This following table were created by addtional thread-->
<div class="box">
<table>
"""

#FIXME:, need to move this to config file.
Key_Italic=True
Font_Size=5
HighLight_msg_tag_start="<hl>"
HighLight_msg_tag_end="</hl>"
START_DOC_DICT=dict(
title="Test_Title",
err_color="#FF0000",
warn_color="#FFFF00",
info_color="#FFFFFF",
dbg_color="#FFFFFF")
log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


class HTMLFileHandler(logging.handlers.RotatingFileHandler):
    """
    File handler specialised to write the start of doc as html and to close it
    properly.
    """
    def __init__(self, filename, mode='a', maxBytes=0,START_OF_DOC_FMT=None,
                 END_OF_DOC_FMT=None, encoding=None, delay=False, 
                 title="Default Title"):
        #Rewrite RotatingFileHandler.__init__()
        self.title=title
        self.start_of_doc_fmt=START_OF_DOC_FMT
        if maxBytes > 0:
            mode = 'a'
        logging.handlers.BaseRotatingHandler.__init__(self, filename,\
                         mode, encoding, delay)
        self.maxBytes = maxBytes-len(self.start_of_doc_fmt)-len(END_OF_DOC_FMT)-3
        # Write header
        with open(self.baseFilename, 'r') as infile:
            data = infile.read()
            #infile.seek(0,2)
            #print('end is:',infile.tell())
            #insert_offset=infile.tell()-18
            #print('will insert to:',insert_offset)

        if self.title in data:
            #self.stream.seek(-18,2)
            #self.stream.write(REM_DOC_FMT)
            #self.stream.seek(0,2)
            self.stream.write(MID_OF_DOC_FMT)
        else:
            self.stream.write(self.start_of_doc_fmt)

    def emit(self, record):
        """
        Rewrite emit for BaseRotatingHandler.emit(self,record)
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:

            if self.shouldRollover(record):
                self.stream.write(END_OF_DOC_FMT)
                self.doRollover()
                self.stream.write(self.start_of_doc_fmt)
            logging.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)

    def doRollover(self):
        """
        Rewrite emit for BaseRotatingHandler.doRollover(self)
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        base_fn=os.path.splitext(self.baseFilename)
        backupCount=1
        while True:
            if not os.path.exists(self.rotation_filename("%s_%d%s" % \
                (base_fn[0],backupCount,base_fn[1]))):
                break
            backupCount+=1
        if backupCount > 0:
            for i in range(backupCount - 1, 0, -1):
                bfn_root, bfn_ext = os.path.splitext(self.baseFilename)
                sfn = self.rotation_filename("%s_%d%s" % (bfn_root,i,bfn_ext))
                dfn = self.rotation_filename("%s_%d%s" % (bfn_root,i+1,bfn_ext))
                if os.path.exists(sfn):
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(base_fn[0] + "_1"+ base_fn[1])
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def close(self):
        # finish document
        self.stream.write(END_OF_DOC_FMT)
        super().close()
    

class HTMLFormatter(logging.Formatter):
    """
    Formats each record in html
    """
    CSS_CLASSES = {'WARNING': 'warn',
                   'INFO': 'info',
                   'DEBUG': 'debug',
                   'CRITICAL': 'err',
                   'ERROR': 'err'}

    def __init__(self, fmt=None):
        super().__init__(fmt)

    def format(self, record):
        try:
            class_name = self.CSS_CLASSES[record.levelname]
        except KeyError:
            class_name = "info"
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        record.cssname=class_name
        # handle '<' and '>' (typically when logging %r)
        #msg = record.msg
        #msg=record.getMessage()
        if Key_Italic:
            record.message=record.message.replace(HighLight_msg_tag_start, \
                             "<font size={0:d}><i>".format(Font_Size))
            record.message=record.message.replace(HighLight_msg_tag_end,\
                             "</i></font>")
        else:
            record.message=record.message.replace(HighLight_msg_tag_start,\
                             "<font size={0:d}>".format(Font_Size))
            record.message=record.message.replace(HighLight_msg_tag_end,\
                             "</font>")
        #msg = msg.replace("<", "&#60")
        #msg = msg.replace(">", "&#62")
        return MSG_FMT % record.__dict__

class CONFormatter(logging.Formatter):
    """
    Formats each record to console
    """
    def __init__(self, fmt=None):
        super().__init__(fmt)

    def format(self, record):

        console_normal='\x1b[0m'
        if record.levelname=='ERROR':
            console_color='\x1b[31m'
        elif record.levelname=='CRITICAL':
            console_color='\x1b[31m'
        elif record.levelname=='WARNING':
            console_color='\x1b[33m'
        else:
            console_color=console_normal

        record.message = record.getMessage()
        record.message=record.message.replace(HighLight_msg_tag_start,\
                       console_color)
        record.message=record.message.replace(HighLight_msg_tag_end,\
                       console_normal)

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s

class PyLogger(logging.Logger):
    """
    Log records to html using a custom HTML formatter and a specialised
    file stream handler.
    """
    def __init__(self, name="html_logger", filename="log.html", mode='a',
                 title="HTML Logger",level=logging.DEBUG, maxBytes=204800,
                 html_format='%(asctime)',encoding=None, delay=False,
                 console_log=False):

        super().__init__(name, level)

        start_of_doc_fmt=START_OF_DOC_FMT % START_DOC_DICT

        format_html = HTMLFormatter(html_format)
        fh = HTMLFileHandler(filename, mode=mode, maxBytes=maxBytes, \
             START_OF_DOC_FMT=start_of_doc_fmt, END_OF_DOC_FMT=END_OF_DOC_FMT,\
             encoding=encoding, delay=delay, title=title)
        fh.setFormatter(format_html)
        self.addHandler(fh)
        if console_log:
            format_con = CONFormatter(html_format)
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(format_con)
            self.addHandler(ch)
