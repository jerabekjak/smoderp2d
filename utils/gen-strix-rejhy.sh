#!/bin/bash
# @@@ - toto nastav

# @@@
indata=tests/data/nucice.save
# @@@
srazka=tests/data/rainfall.txt

echo "" > run

for i in 0.001 0.05 0.5 # sklon @@@
do
	for j in 0.001 0.05 0.5 # hcrit @@@
	do
		file_=tests/test-$i-$j.ini
		log_=test-$i-$j.log
		output_=test-$i-$j
		echo $file_
		echo "# # Configure file for cmd run of smoderp2d model. # #" > $file_
		echo "" >> $file_
		echo "# Smoderp2d can be executed (run) from the commandline on linux machine." >> $file_
		echo "" >> $file_
		echo "# Most of the input data have to be provided in pickle file" >> $file_
		echo "# if smoderp2d is run in cmd mode. The pickle file is created" >> $file_
		echo "# in data preparation only option is set in a give gis" >> $file_
		echo "# software" >> $file_
		echo "" >> $file_
		echo "# If yo choose this option of running smoderp2d:" >> $file_
		echo "#   (1) Some parameters stored in pickle file cannot be changed." >> $file_
		echo "#       Those inputs are set to "dash" in this configuration file." >> $file_
		echo "#   (2) Some parameters are mandatory and used only for" >> $file_
		echo "#       the cmd run. This is documented above affected parameters" >> $file_
		echo "" >> $file_
		echo "[sklon-hcrit]" > $file_
		echo "sklon:" $i >> $file_
		echo "hcrit:" $j >> $file_
		echo "X: 20" >> $file_
		echo "Y: 0.5" >> $file_
		echo "b: 1.5" >> $file_
		echo "Ks: 1e-6" >> $file_
		echo "S: 1e-5" >> $file_
		echo "# zaporne cislo v metrech" >> $file_
		echo "ret: -0.1" >> $file_
		echo "" >> $file_
		echo "" >> $file_
		echo "" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "[GIS]" >> $file_
		echo "dem: -" >> $file_
		echo "soil: -" >> $file_
		echo "lu: -" >> $file_
		echo "" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "[shape atr]" >> $file_
		echo "soil-atr: -" >> $file_
		echo "lu-atr: -" >> $file_
		echo "" >> $file_
		echo "# file with the rainfall record" >> $file_
		echo "# the rainfall can be changed in cmd run." >> $file_
		echo "# if file: - the rainfall in pickle file is used." >> $file_
		echo "[rainfall]" >> $file_
		echo "file: "$srazka >> $file_
		echo "#file: -" >> $file_
		echo "" >> $file_
		echo "[time]" >> $file_
		echo "# maximum and initial time" >> $file_
		echo "#sec" >> $file_
		echo "maxdt: 30" >> $file_
		echo "# end time of simulations" >> $file_
		echo "#min" >> $file_
		echo "endtime: 60" >> $file_
		echo "" >> $file_
		echo "[Other]" >> $file_
		echo "# Path to the pickle file" >> $file_
		echo "indata: "$indata >> $file_
		echo "#" >> $file_
		echo "# output directory" >> $file_
		echo "# content of the directory is erased at the beginning of the program" >> $file_
		echo "outdir: tests/data/"$output_ >> $file_
		echo "# type of processes involved" >> $file_
		echo "# default si 3" >> $file_
		echo "# 0 - sheet runoff" >> $file_
		echo "# 1 - sheet and rill runoff" >> $file_
		echo "# 2 - sheet, rill and subsurface runoff" >> $file_
		echo "# 3 - sheet, rill and stream runoff" >> $file_
		echo "typecomp: 3" >> $file_
		echo "# Mfda zatim zustava false" >> $file_
		echo "mfda: False" >> $file_
		echo "# for linux must be False or false" >> $file_
		echo "arcgis: false" >> $file_
		echo "# extraout: True for detailed output" >> $file_
		echo "# default: False" >> $file_
		echo "extraout: True" >> $file_
		echo "# data loaded and only computation is performer for roff option" >> $file_
		echo "# for cmd run ONLY roff is possible" >> $file_
		echo "partialcomp: roff" >> $file_
		echo "#" >> $file_
		echo "# logging level" >> $file_
		echo "#  - CRITICAL" >> $file_
		echo "#  - ERROR" >> $file_
		echo "#  - WARNING" >> $file_
		echo "#  - INFO" >> $file_
		echo "#  - DEBUG" >> $file_
		echo "#  - NOTSET" >> $file_
		echo "logging: DEBUG" >> $file_
		echo "#" >> $file_
		echo "# experimental" >> $file_
		echo "# times when rasters will be printed" >> $file_
		echo "# default: off for '-' or empty value" >> $file_
		echo "printtimes:" >> $file_
		echo "#" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "points: -" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "soilvegtab : -" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "soilvegcode : -" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "streamshp :  -" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "streamtab: -" >> $file_
		echo "# cannot be set in cmd run" >> $file_
		echo "streamtabcode: -" >> $file_


		echo "./bin/start-smoderp2d.py --typecomp roff --indata " $file_" > "$log_ >> run

	done
done

