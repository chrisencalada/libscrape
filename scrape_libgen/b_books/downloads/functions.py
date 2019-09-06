def request_with_proxies():
# function takes a url and calls the requests library to find sites' html content and return it
# function will use a revolving list of user-agents and proxies scraped from proxy lists to do this
# will return page content that will be used by soup_for_libgen to extract the page content
# need to create the following tests
# 1. make sure that you can get a response back from the url that you are calling
# 2. make sure that your proxies are working
# 3. make sure that you are scraping the correct proxy list websites 
	return

def request_with_multithreading():
# function is used to speed up request_with_proxies and will have request_with_proxies as its input and
# return page content
	return

def soup_for_libgen():
# function will be used to extract the necessary data from websites generated by either request_with_proxies
# or request_with_multithreading. Function will be site specific since each website has different html structures
# willl return 
	return

