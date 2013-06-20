PY_VERSIONS = 2.6 2.7 3.2

.PHONY : .envs

test:
	python setup.py test

$(eval .envs : $(foreach v,$(PY_VERSIONS),.envs/py$(v)))
$(eval test-envs : $(foreach v,$(PY_VERSIONS),test-$(v)))

.envs/py%:
	mkdir -p .envs
	virtualenv --distribute -p `which python$*` .envs/py$*

test-% :
	./.envs/py$*/bin/python setup.py test
