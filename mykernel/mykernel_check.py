#
##!/bin/bash
#if [ $# -ne 0 ]
#then
#  echo "Programa que chequea la integridad de vmlinuz y myinit.gz"
#  echo "Después se debe ejecutar: # mykernel.check"
#fi
#echo "HMAC Password"
#read -s password
#
#cd /boot
#hmac256 $password vmlinuz > vmlinuz.hmac.last
#hmac256 $password myinit.gz > myinit.hmac.last
#
#diff /boot/vmlinuz.hmac.last /usr/src/vmlinuz.hmac
#diff /boot/myinit.hmac.last /usr/src/myinit.hmac
