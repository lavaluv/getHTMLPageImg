from selenium import webdriver
import os
import time
import re

fileName = "url1.txt"
with open (fileName,'r') as file_to_read:
	while True:
		url = file_to_read.readline()
		# url = ''.join(url).strip("\n")
		print(url)
		if not url:
			break
		driver = webdriver.PhantomJS(executable_path = "/Users/lava/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs")
		#driver = webdriver.Firefox()
		try:
			driver.get(url)
		except Exception as e:
			print('error page')
		page = driver.page_source
		fileStr = 'picture/'
		dirname = os.path.dirname(fileStr)
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		driver.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    	""")

		for i in xrange(30):
			if "scroll-done" in driver.title:
				break
			time.sleep(10)
		reg1 = re.compile("^http://")
		reg2 = re.compile("^https://")
		picName1 = reg1.sub('',url)
		picName2 = reg2.sub('',picName1)
		driver.save_screenshot(fileStr+picName2+'.png')
		assert "No results found." not in driver.page_source
		driver.close()
	pass
file_to_read.close()