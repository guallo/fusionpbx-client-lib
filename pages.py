import re

from selenium.webdriver.support.ui import Select

from .constants import *


class Page:
    def __init__(self, wdriver):
        self._wdriver = wdriver
    
    def get_webdriver(self):
        return self._wdriver
    
    def get_base_url(self):
        return re.search('^https?://[^/]+', self._wdriver.current_url).group(0)


class LoginPage(Page):
    USERNAME_INPUT = '[name="username"]'
    PASSWORD_INPUT = '[name="password"]'
    LOGIN_BUTTON = '#btn_login'
    
    def login(self, username, password):
        username_input = self._wdriver.find_element_by_css_selector(
                        self.USERNAME_INPUT)
        username_input.send_keys(username)
        
        password_input = self._wdriver.find_element_by_css_selector(
                        self.PASSWORD_INPUT)
        password_input.send_keys(password)
        
        login_button = self._wdriver.find_element_by_css_selector(
                        self.LOGIN_BUTTON)
        login_button.click()
        return DashboardPage(self._wdriver)


class LoggedInPage(Page):
    DOMAIN_SELECTOR_LINK = '.domain_selector_domain'
    DOMAIN_FILTER_INPUT = '#domain_filter, #domains_filter'
    
    def logout(self):
        self._wdriver.get(self.get_base_url() + '/logout.php')
        return LoginPage(self._wdriver)
    
    def change_to_domain(self, domain):
        domain_selector_link = self._wdriver.find_element_by_css_selector(
                                self.DOMAIN_SELECTOR_LINK)
        domain_selector_link.click()
        
        domain_filter_input = self._wdriver.find_element_by_css_selector(
                                self.DOMAIN_FILTER_INPUT)
        domain_filter_input.send_keys(domain)
        
        domain_item = self._wdriver.find_element_by_id(domain)
        domain_item.click()
        return DashboardPage(self._wdriver)
    
    def goto_call_flows(self):
        self._wdriver.get(self.get_base_url() + '/app/call_flows/call_flows.php')
        return CallFlowsPage(self._wdriver)


class DashboardPage(LoggedInPage):
    pass


class CallFlowsPage(LoggedInPage):
    NAME_LINKS = '.list-row > td:nth-child(2) > a:nth-child(1)'
    
    def edit(self, name):
        name_links = self._wdriver.find_elements_by_css_selector(
                    self.NAME_LINKS)
        
        matched_name_links = list(filter(lambda nl: nl.text == name, name_links))
        
        assert matched_name_links, f'could not find the call flow with name {name}'
        
        matched_name_links[0].click()
        return CallFlowEditPage(self._wdriver)


class CallFlowEditPage(LoggedInPage):
    STATUS_SELECT = '[name="call_flow_status"]'
    SAVE_BUTTON = '#btn_save'
    
    def save(self, status=Value.CURRENT_VALUE):
        if status is not Value.CURRENT_VALUE:
            status_value_map = {
                None: '', 
                True: 'true', 
                False: 'false'}
            status_select = self._wdriver.find_element_by_css_selector(
                            self.STATUS_SELECT)
            Select(status_select).select_by_value(status_value_map[status])
        
        save_button = self._wdriver.find_element_by_css_selector(
                        self.SAVE_BUTTON)
        save_button.click()
        return CallFlowsPage(self._wdriver)
    
    def get_values(self):
        values = {}
        
        status_value_inv_map = {
                '': None, 
                'true': True, 
                'false': False}
        status_select = self._wdriver.find_element_by_css_selector(
                        self.STATUS_SELECT)
        inv_status = Select(status_select).first_selected_option.get_attribute('value')
        values['status'] = status_value_inv_map[inv_status]
        
        return values
