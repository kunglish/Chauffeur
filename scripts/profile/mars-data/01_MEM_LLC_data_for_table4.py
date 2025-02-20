### Script for Table 4. .  Comparison of memory access and main memory (DRAM) bandwidth (B/W) of Chauffeur applications on the Jetson TX2
### Measured numbers are only from CPU performance counters and do not consider memory traffic from GPU. Unit is million-transfers/sec(MT/s)
import sys
import os
import numpy as np
import pandas as pd
from statistics import mean
from scipy import stats

# Please adjust if applications are misclassified
POWER_CLASSIFY_MARGIN=0.2

def find_files(dir) -> list:
    result = []
    for filename in os.listdir(dir):
        if filename.endswith("-fine_trace.csv"):
            result.append(str(filename))
    return [result, dir]


def filter(name, data):
    gpu_power_mean = data["power_gpu_w"].mean()
    cpu_power_mean = data["power_cpu_w"].mean()
    
    diff_GPU = data["power_gpu_w"].max() - gpu_power_mean

    # Check if GPU App
    if diff_GPU > POWER_CLASSIFY_MARGIN:
        print ("[GPU] ", end='')
        tmp = data.loc[abs(data['power_gpu_w'] > gpu_power_mean)]
        data = data[data['sample_id']>=tmp.sample_id.min()]
        data = data[data['sample_id']<=tmp.sample_id.max()]
        # print ("Cutoff: ",gpu_power_mean, ", Min : ", tmp.sample_id.min(), ", Max : ", tmp.sample_id.max(),)
    else:
        print ("[CPU] ", end='')
        
        # These applications have an initialization phase
        if (name == 'lidar-tracking' or name == 'orb-slam-3' ):
            # The following logic tries to discount the init phase when
            # calculating the mean
            cpu_power_mean=cpu_power_mean+1
            tmp = data.loc[abs(data['power_cpu_w'] > cpu_power_mean)]
            data = data[data['sample_id']>=tmp.sample_id.min()]
            data = data[data['sample_id']<=tmp.sample_id.max()]
            # print ("Cutoff: ",cpu_power_mean, ", Min : ", tmp.sample_id.min(), ", Max : ", tmp.sample_id.max(),)

    return data

def process(files:list) -> list:
    output = []
    os.chdir(files[1])
    for i in files[0]:
        data = pd.read_csv(i,delimiter=";")
        name = i[:-15].replace("_", "-")
       
        # Remove warm-up and exit phases
        data=filter(name, data)

        data = data.sort_values(by=["total_llc_misses"])
        data_possible_outlier = data[data["total_llc_misses"].between(data["total_llc_misses"].quantile(0.99), data["total_llc_misses"].quantile(1),inclusive = True)]
        data_none_outliers = data[data["total_llc_misses"].between(data["total_llc_misses"].quantile(0), data["total_llc_misses"].quantile(0.99), inclusive = False)]
        none_outlier_max = data_none_outliers["total_llc_misses"].max()

        for j in data_possible_outlier["total_llc_misses"]:
            if j <= none_outlier_max*1.7:
                data_none_outliers = data_none_outliers.append(data_possible_outlier[data_possible_outlier["total_llc_misses"] == j])

        temp = [name, data_none_outliers["total_mem_access"].mean(), data_none_outliers["total_mem_access"].max(),  data_none_outliers["total_llc_misses"].mean(), data_none_outliers["total_llc_misses"].max()]
        
        for index in range(1,5):
            temp[index] = int( (temp[index]*20)/(10**6))
        output.append(temp)
        print(temp)
    return output

def write_file(data:list):
    col = ['ApplicationName', 'AvgTotalMemAccess', 'PeakTotalMemAccess', 'AvgTotalLlcMisses', 'PeakTotalLlcMisses']
    new_data = pd.DataFrame(data, columns = col)
    new_data = new_data.sort_values(by=['PeakTotalMemAccess','PeakTotalLlcMisses', 'AvgTotalMemAccess', 'AvgTotalLlcMisses'])
    df_1 = new_data.iloc[0:1]
    df_2 = new_data.iloc[1:]   
    df_2 = df_2.sort_values(by = ['ApplicationName'])
    new_data = pd.concat([df_1, df_2])
    new_data.to_csv("mem-llc.csv", index=False)

    data = pd.read_csv("mem-llc.csv",delimiter=",", index_col = 0)
    data = data.transpose()
    data = data.reset_index()
    data.to_csv("mem-llc.csv", index=False)

if __name__ == "__main__":
    FileList = find_files( str(sys.argv[1]) )
    DataOutput = process(FileList)
    write_file(DataOutput)
