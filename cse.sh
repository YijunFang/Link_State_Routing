#!/bin/bash
gnome-terminal -e "bash -c \"python Lsr.py A 2000 configA.txt; exec bash\"" &
if false
then
gnome-terminal -e "bash -c \"python Lsr.py B 2001 configB.txt; exec bash\"" &
gnome-terminal -e "bash -c \"python Lsr.py C 2002 configC.txt; exec bash\"" &
gnome-terminal -e "bash -c \"python Lsr.py D 2003 configD.txt; exec bash\"" &
gnome-terminal -e "bash -c \"python Lsr.py E 2004 configE.txt; exec bash\"" &
gnome-terminal -e "bash -c \"python Lsr.py F 2005 configF.txt; exec bash\"" &
fi
