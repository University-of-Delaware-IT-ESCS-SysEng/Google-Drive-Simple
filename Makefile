BASEFILE=sa
BASEFILER=sa-r
BASE_PYTHON=python3

MODULES=sa_app/drive.py \
sa_app/our_auth.py \
sa_app/error.py

bin:
	echo '#!/bin/bash' > ${BASEFILE}
	echo "env PYTHONPATH=${PWD} ${PWD}/env/bin/python -m sa_app.sa "$$\* >> ${BASEFILE}
	chmod 775 ${BASEFILE}
	echo '#!/bin/bash' > ${BASEFILER}
	echo "env PYTHONPATH=${PWD} ${PWD}/env/bin/python -m sa_app.sa_r "$$\* >> ${BASEFILER}
	chmod 775 ${BASEFILER}

env: bin
	rm -rf env/
	${BASE_PYTHON} -m venv env
	env/bin/python -m pip install -r requirements.txt
