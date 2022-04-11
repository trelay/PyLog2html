#!/usr/bin/env python3
import logging
import unittest

expected_html_results = ['<table id="toptable" style="table-layout: fixed; width: 100%">',
                         '<td class="debug">This is debug</td>',
                         '<td class="info">This is info</td>',
                         '<td class="warn">This is <font size=5><i>warning</i></font></td>',
                         '<td class="err">This is <font size=5><i>error</i></font> xxx</td>',
                         '<td class="info">_____________</td>',
                         '<td class="info">Add html table:<table><tr><th>column1</th>',
                         '<td class="info">log with extra params</td>',
                         '<td class="info">foo=bar</td>',
                         '<th>column2</th></tr><tr><th>column1</th><th>column2</th></tr></table></td>']


class Test(unittest.TestCase):
    def setUp(self):
        from HTMLLogger import HTMLLogger
        self.log_nm = "log.html"
        self.logger = HTMLLogger(name="Test_App", html_filename=self.log_nm ,console_log=True)

    def tearDown(self):
        import os
        logging.shutdown()
        os.remove(self.log_nm)

    def test_logger(self):
        logger = self.logger
        for _ in range(1):
            logger.debug('This is debug')
            logger.info('This is info')
            logger.warning("This is <hl>warning</hl>")
            logger.error('This is <hl>error</hl> xxx')
            logger.info('_____________')
            logger.info("log with extra params", extra={"foo": "bar"})
            logger.table('Add html table:<table><tr><th>column1</th><th>column2</th></tr>'
                         '<tr><th>column1</th><th>column2</th></tr></table>')
        with open(self.log_nm, "r") as log_file:
            html_log = log_file.read()

        for expected in expected_html_results:
            assert expected in html_log

if __name__=="__main__":
    unittest.main()
