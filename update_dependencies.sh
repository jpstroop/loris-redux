#!/bin/bash
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
pip freeze | grep -v "pkg\-resources" > requirements.txt
echo "*************************************************"
echo "Note: You still need to update setup.py manually!"
echo "*************************************************"
