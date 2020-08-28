from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from .pages import LoginPage


class FPBXContext:
    def __init__(self, base_url, geckodriver_bin=None, firefox_bin=None, 
                headless=None, timeout=None, log_path=None, log_level=None):
        self._base_url = base_url
        self._geckodriver_bin = geckodriver_bin
        self._firefox_bin = firefox_bin
        self._headless = headless
        self._timeout = timeout
        self._log_path = log_path
        self._log_level = log_level
        
        self._wdriver = None
    
    def get_base_url(self):
        return self._base_url
    
    def get_geckodriver_bin(self):
        return self._geckodriver_bin
    
    def get_firefox_bin(self):
        return self._firefox_bin
    
    def get_headless(self):
        return self._headless
    
    def get_timeout(self):
        return self._timeout
    
    def get_log_path(self):
        return self._log_path
    
    def get_log_level(self):
        return self._log_level
    
    def create_webdriver(self):
        kwargs = {}
        o = Options()
        
        if self._geckodriver_bin is not None:
            kwargs['executable_path'] = self._geckodriver_bin
        if self._firefox_bin is not None:
            kwargs['firefox_binary'] = self._firefox_bin
        if self._headless is not None:
            o.headless = self._headless
            kwargs['options'] = o
        if self._log_path is not None:
            kwargs['service_log_path'] = self._log_path
        if self._log_level is not None:
            o.log.level = self._log_level
            kwargs['options'] = o
        
        wdriver = Firefox(**kwargs)
        
        if self._timeout is not None:
            wdriver.implicitly_wait(self._timeout)
        
        try:
            wdriver.get(self._base_url)
        except WebDriverException as exception:
            wdriver.quit()
            raise
        
        return wdriver
    
    def __enter__(self):
        self._wdriver = self.create_webdriver()
        return LoginPage(self._wdriver)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._wdriver.quit()
