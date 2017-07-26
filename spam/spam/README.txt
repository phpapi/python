== filterserver ==

easy_install tornado

cd ../libs/ahocorasick-1.0pre/
python setup.py build

cd ../../spam
python filterserver.py


TODO: http://supervisord.org/configuration.html


