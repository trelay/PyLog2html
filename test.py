#!/usr/bin/env python3
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        from HTMLLogger import HTMLLogger
        self.log_nm = "log.html"
        self.logger = HTMLLogger(name="Test_App", html_filename=self.log_nm ,console_log=True)

    def tearDown(self):
        import os
        os.remove(self.log_nm)

    def test_logger(self):
        logger = self.logger
        for i in range(1):
            logger.debug('This is debug')
            logger.info('This is info')
            logger.warning("This is <hl>warning</hl>")
            logger.error('This is <hl>error</hl> xxx')
            logger.info('_____________')
            logger.table('Add html table:<table><tr><th>...</th></tr></table>')
if __name__=="__main__":
    unittest.main()
