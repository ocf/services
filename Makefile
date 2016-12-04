.PHONY: test
test:
	tox

.PHONY: deploy
deploy:
	./deploy.py

.PHONY: diff
diff:
	./deploy.py --diff-only
