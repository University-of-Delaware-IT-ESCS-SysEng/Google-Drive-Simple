BASEFILE=sa
BASE_PYTHON=python3.11

MODULES=sa_app/drive.py \

bin:
	echo '#!/bin/bash' > ${BASEFILE}
	echo "env PYTHONPATH=${PWD} ${PWD}/env/bin/python -m sa_app.sa "$$\* >> ${BASEFILE}
	chmod 775 ${BASEFILE}

env: bin
	rm -rf env/
	${BASE_PYTHON} -m venv env
	env/bin/python -m pip install -r requirements.txt
