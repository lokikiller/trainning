#/!bin/bash
read -sp "Enter a password: " pass

if test "${pass}" == "123456"
then
    echo -e "\nsuccess"
    exit 0
else 
    echo -e "\nerror"
    exit 1
fi
