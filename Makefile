#WEBPY_ENV = test

depends:
	pip install -r requirements.txt

thriftserve:
	python ./server.py

webserve:
	python ./webapp.py $(WEBPY_LISTEN)

#tests:
#	WEBPY_ENV=$(WEBPY_ENV) nosetests
