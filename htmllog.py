#!/usr/bin/python3
"""
Python log file to html and do rotation method,but without limited count.
Usage:
 - call setup and specify the filename, title, version and level
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
width: 1000px;
font-family: Arial;
font-size: 16px;
color: #C0C0C0;
}
h1 {
color : #FFFFFF;
border-bottom : 1px dotted #888888;
}
pre {
font-family : arial;
margin : 0;
}
.box {
border : 1px dotted #818286;
padding : 5px;
margin: 5px;
width: 950px;
background-color : #292929;
}
.err {
color: #FF0000;
font-weight: bold
}
.warn {
color: #FFFF00;
font-weight: bold
}
.info {
color: #FFFFFF;
}
.debug {
color: #FFFFFF;
}
</style>
</head>
<body>
<h1>%(title)s</h1>
<h3>%(version)s</h3>
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
<td class="%(cssname)s"><pre>%(message)s</pre></td>
<tr>
"""

MID_OF_DOC_FMT = """
<!--
This following table were created by addtional thread-->
<div class="box">
<table>
"""
RM_END_DOC_FMT="""
</body>
</html>
"""


class HTMLFileHandler(logging.handlers.RotatingFileHandler):
    """
    File handler specialised to write the start of doc as html and to close it
    properly.
    """
    def __init__(self, filename, mode='a', maxBytes=0,START_OF_DOC_FMT=None,
                 END_OF_DOC_FMT=None, encoding=None, delay=False):
        title="TEST_Title"
        #Rewrite RotatingFileHandler.__init__()
        if maxBytes > 0:
            mode = 'a'
        logging.handlers.BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes-len(START_OF_DOC_FMT)-len(END_OF_DOC_FMT)-3
        # Write header
        with open(self.baseFilename, 'r') as infile:
            data = infile.read()
            #infile.seek(0,2)
            #print('end is:',infile.tell())
            #insert_offset=infile.tell()-18
            #print('will insert to:',insert_offset)

        if title in data:
            #self.stream.seek(-18,2)
            #self.stream.write(REM_DOC_FMT)
            #self.stream.seek(0,2)
            self.stream.write(MID_OF_DOC_FMT)
        else:
            self.stream.write(START_OF_DOC_FMT % {"title": title,
                          "version": '1.3'})

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
                self.stream.write(START_OF_DOC_FMT % {"title": "TEST_Title",
                                         "version": '1.3'})
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
                #sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
                #dfn = self.rotation_filename("%s.%d" % (self.baseFilename, i+1))
                bfn_root, bfn_ext = os.path.splitext(self.baseFilename)
                sfn = self.rotation_filename("%s_%d%s" % (bfn_root,i,bfn_ext))
                dfn = self.rotation_filename("%s_%d%s" % (bfn_root,i + 1,bfn_ext))
                if os.path.exists(sfn):
                    #if os.path.exists(dfn):
                    #    os.remove(dfn)
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
        #msg = msg.replace("<", "&#60")
        #msg = msg.replace(">", "&#62")
        return MSG_FMT % record.__dict__


class HTMLLogger(logging.Logger):
    """
    Log records to html using a custom HTML formatter and a specialised
    file stream handler.
    """
    def __init__(self,
                 name="html_logger",
                 level=logging.DEBUG,
                 filename="log.html", mode='w',
                 title="HTML Logger", version="1.0.0"):
        super().__init__(name, level)
        f = HTMLFormatter( '%(asctime) ')
        h = HTMLFileHandler(filename, mode=mode, maxBytes=2000, \
            START_OF_DOC_FMT=START_OF_DOC_FMT, END_OF_DOC_FMT=END_OF_DOC_FMT)
        h.setFormatter(f)
        self.addHandler(h)
