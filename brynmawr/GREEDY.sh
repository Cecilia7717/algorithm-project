#!/bin/sh

for i in $(seq 2000 2014); do
    #python3 /home/zchen4/340/brynmawr/get_bmc_info.py /home/zchen4/340/brynmawr/data/Fall${i}.csv /home/zchen4/340/brynmawr/studentpref/studentpref_Fall_${i}.txt /home/zchen4/340/brynmawr/constrains/constrains_Fall_${i}.txt
    echo "Fall $i"  
    start_time=$(date +%s) 
    time python3 alg_timeslot_greedy.py /home/zchen4/340/brynmawr/constrains/constrains_Fall_${i}.txt /home/zchen4/340/brynmawr/studentpref/studentpref_Fall_${i}.txt /home/zchen4/340/brynmawr/schedule_Greedy/schedule_Fall_${i}.txt
    end_time=$(date +%s)
    duration=$(( end_time - start_time ))
    # echo "Fall $i completed in ${duration} seconds."
done

for i in $(seq 2001 2015); do
    echo "Spring $i"    
    start_time=$(date +%s)
    time python3 alg_timeslot_greedy.py /home/zchen4/340/brynmawr/constrains/constrains_Spring_${i}.txt /home/zchen4/340/brynmawr/studentpref/studentpref_Spring_${i}.txt /home/zchen4/340/brynmawr/schedule_Greedy/schedule_Fall${i}.txt
    end_time=$(date +%s)
    duration=$(( end_time - start_time ))
    # echo "Spring $i completed in ${duration} seconds."
done