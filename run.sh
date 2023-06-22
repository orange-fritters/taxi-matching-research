#!/bin/bash

exp_name="effect_c"

# Create experiment directory
mkdir -p results/${exp_name}

# Initialize CSV file with headers
echo "time_window,tolerance,a,b,c,mean_time,equity" > results/${exp_name}/_results.csv

# Initialize description file
description_file="results/${exp_name}/_description.txt"
echo "Experiment settings:" > ${description_file}
echo "Data path: data/output.csv" >> ${description_file}
echo "Total time: 180" >> ${description_file}
echo "Experiment name: ${exp_name}" >> ${description_file}
echo "Variations:" >> ${description_file}
echo "Time window: 1 to 10" >> ${description_file}
echo "Tolerance: 0 to 10" >> ${description_file}
echo "a: 0 to 1.0 in increments of 0.1" >> ${description_file}
echo "b: 1.0 to 0 in increments of 0.1" >> ${description_file}
echo "!!! Testing peak time with the above range" >> ${description_file}

total_runs=$((5 * 15 * 4))
count=0
start_time=$(date +%s)

for time_window in $(seq 1 1 1)
do
  for tolerance in $(seq 1 1 1)
  do
    for a in $(seq 0.0 0.1 1.0)
    do
      b=$(echo "1.0 - $a" | bc)
      c=100

      # Run experiment and capture output (assumes mean_time is printed by main.py)
      output=$(python3 main.py \
        --data_path './data/output.csv' \
        --total_time 180 \
        --time_window ${time_window} \
        --tolerance ${tolerance} \
        --a ${a} \
        --b ${b} \
        --c ${c} \
        --exp_name ${exp_name})

      IFS=', ' read -r -a array <<< "$output"
      mean_time="${array[0]}"
      equity="${array[1]}"

      # Write results to CSV file
      echo "${time_window},${tolerance},${a},${b},${c},${mean_time},${equity}" >> results/${exp_name}/_results.csv

      count=$((count+1))

    done
    percent_done=$(echo "scale=2; ($count / $total_runs) * 100" | bc)
    elapsed_time=$(($(date +%s) - start_time))
    eta=$(echo "scale=2; (($total_runs / $count) * $elapsed_time) / 3600" | bc)
    echo "Completed ${percent_done}% of runs. Estimated time remaining: ${eta} hours."
  done
done

end_time=$(date +%s)
total_time=$(echo "scale=2; ($end_time - $start_time) / 3600" | bc)
echo "Total experiment time: ${total_time} hours."
