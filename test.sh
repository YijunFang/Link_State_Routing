!/bin/sh
./use.sh "python Lsr.py A 2000 Topology1/configA.txt" &
./use.sh "python Lsr.py B 2001 Topology1/configB.txt" &
./use.sh "python Lsr.py C 2002 Topology1/configC.txt" &
./use.sh "python Lsr.py D 2003 Topology1/configD.txt" &
./use.sh "python Lsr.py E 2004 Topology1/configE.txt" &
./use.sh "python Lsr.py F 2005 Topology1/configF.txt"
wait

# ./use.sh "python Lsr.py A 2000 configA.txt" &
# ./use.sh "python Lsr.py B 2001 configB.txt" &
# ./use.sh "python Lsr.py C 2002 configC.txt" &
# ./use.sh "python Lsr.py D 2003 configD.txt" &
# ./use.sh "python Lsr.py E 2004 configE.txt" &
# ./use.sh "python Lsr.py F 2005 configF.txt"

# wait
