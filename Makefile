.PHONY: test
test: venv install-hooks
	tox

venv: vendor/venv-update requirements-dev.txt
	vendor/venv-update venv= $@ -ppython3 install= -r requirements-dev.txt

.PHONY: install-hooks
install-hooks: venv
	venv/bin/pre-commit install -f --install-hooks

.PHONY: clean
clean:
	rm -rf venv

.PHONY: deploy
deploy:
	./deploy.py

.PHONY: diff
diff:
	./deploy.py --diff-only
