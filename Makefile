# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @GPLv3 License
# @http://tasdikrahman.me

clean:
	-find . -name '*.pyc' -delete
	-find . -name '__pycache__' -delete

run:
	python run.py start

bot_id:
	python run.py bot_id

deps:
	pip install -r requirements.txt

deploy: clean
	# deploys app to heroku as well pushes the latest commits to the github
	# remote
	git push -u origin master
	git push -u heroku master

force-deploy: clean
	## DONT DO THIS! EVEN IF THE WORLD COMES TO AN END!
	git push -u origin master --force
	git push -u heroku master --force

.PHONY: help
help:
	@echo "\nPlease call with one of these targets:\n"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F:\
        '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}'\
        | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs | tr ' ' '\n' | awk\
        '{print "    - "$$0}'
	@echo "\n"
