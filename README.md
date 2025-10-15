# TOF_sensor_vl53l4cx
1) The .project file is for stm ide to interface with the microcontroller - STM32 NUCLEO64F411RE board 
2) The tof_side.py code is for connecting with the gantry to automate the process of taking readings, this involves taking the readings for a particular distance after recieving the acknowledgement. this makes sure that we dont take any reading during the transience.
3) the setup is done for grey target 
4) this is the link for all the csv data taken at different distances for 40 secs - https://drive.google.com/drive/folders/1jUvgsX_affJ1PpiAoaE1oB-96LMEpyfm?usp=sharing
   it includes the error analysis results along with the code in ipynb file
5) similarly readings taken without lights along with its analysis result - https://drive.google.com/drive/folders/1KHmUzAsaaba-AjyzeVhUJRJ9S7V3WAbV?usp=sharing

# Analysis results 
1) Very negligible data points have errors that lie in the +-5% range of true distance (almost 0%) results in vl53l4cx_summary_sheet.csv
2) if we take the envolope of range ( i.e +-5% of true value ) centered around measured mean then almost all points fit the condition, but this is not a good way as the measured mean will change with number of readings taken. result in - accuracy_summary_compare_wrt_mean.csv
3) if we keep the envolope to be (-5% * T + 25 , +5% * T + 40) then also all the readings lie in the region, ( 25 and 40 are not optimised values, T is true distance) the results of this are there in accuracy_summary_with_constants.csv
4) the errors are discrete as shown in the histogram of the <img width="767" height="486" alt="image" src="https://github.com/user-attachments/assets/08d88a73-11ee-4792-baed-7b0810850783" />

 


