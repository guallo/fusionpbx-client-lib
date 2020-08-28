# fusionpbx-client-lib

## Dependencies:

*  python3
*  selenium
*  firefox
*  geckodriver

## Usage example:

```bash
~$ git clone https://github.com/guallo/fusionpbx-client-lib.git fpbx_client_lib
~$ python3
>>> from fpbx_client_lib.fpbx_context import FPBXContext
>>> with FPBXContext('https://host', '/path/to/geckodriver', '/path/to/firefox',
...                 True, 10, '/path/to/geckodriver.log', 'warn') as login_page:
...     dashboard_page = login_page.login('username', 'password')
...     dashboard_page.change_to_domain('some.domain')
...     call_flows_page = dashboard_page.goto_call_flows()
...     call_flow_edit_page = call_flows_page.edit('Some Call Flow')
...     call_flow_edit_page.save(status=False)
...     call_flows_page.logout()
...
>>> 
```
