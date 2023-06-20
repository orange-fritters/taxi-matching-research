#!/bin/zsh

exp_name="bugfix"

# Create experiment directory
mkdir -p results/${exp_name}

# Initialize CSV file with headers
echo "time_window,tolerance,a,b,mean_time" > results/${exp_name}/_results.csv

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

total_runs=$((10 * 11 * 11))
count=0
start_time=$(date +%s)

for time_window in {1..10}
do
  for tolerance in {0..10}
  do
    for a in $(seq 0 0.1 1.0)
    do
      b=$(echo "1.0 - $a" | bc)
      # Run experiment and capture output (assumes mean_time is printed by main.py)
      mean_time=$(python3 main.py \
        --data_path './data/output.csv' \
        --total_time 180 \
        --time_window ${time_window} \
        --tolerance ${tolerance} \
        --a ${a} \
        --b ${b} \
        --exp_name ${exp_name})

      # Write results to CSV file
      echo "${time_window},${tolerance},${a},${b},${mean_time}" >> results/${exp_name}/_results.csv

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
