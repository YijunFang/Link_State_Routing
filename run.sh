#!/bin/bash
gnome-terminal -e "bash -c \"python Lsr.py A 2000 configA_.txt; exec bash\"" &


gnome-terminal -e "bash -c \"python Lsr.py B 2001 configB_.txt; exec bash\"" &
#gnome-terminal -e "bash -c \"python Lsr.py C 2002 configC_.txt; exec bash\"" &
#gnome-terminal -e "bash -c \"python Lsr.py D 2003 configD_.txt; exec bash\"" &
