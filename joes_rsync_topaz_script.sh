#!/usr/bin/env bash

##################################
###### Machine Specific Values ######
MACHINE=topaz.erdc.hpc.mil
CENTER=/p/work2/jhamman/
#################################

rsync -rh -a -v --update --include '*/' --include='*tar.gz' -e "ssh -l $USER" $MACHINE:$CENTER/processed/ . 

