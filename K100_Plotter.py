#Nick Mast
#June 2018

###############################################################################
#K100_Plotter
#
# A script to retrieve and display K100 temperature and HV log data
###############################################################################

###############################################################################
# this is the standard boilerplate that allows this to be run from the command line
###############################################################################
if __name__ == '__main__':
	import sys
	import os
	from datetime import datetime,timedelta
	import subprocess
	import matplotlib
	matplotlib.use('Agg')
	import pandas as pd
	import bisect
	import matplotlib.pyplot as plt
	import numpy as np
	
	#Get the relevant log file
	#Files are copied to "/data/chocula/k100/k100_log/"
	# and are given names of the format "YYYYMMDD_log.txt"
	# The tab separated format is as follows

	#time [s]        H35_Tplot [K]   HP 3478A [V]    Keithley 617 [V]
	#1528127129      0.034631        -0.148965       -0.000084
	#1528127134      0.034621        -0.149311       -0.000081
	#...

	
	#######################
	#Build the filenames for today and yesterday
	#######################
	directoryName="/data/chocula/k100/k100_log/"
	fileNameToday=datetime.now().strftime("%Y%m%d")+"_log.txt"
	fileNameYesterday=(datetime.now() - timedelta(days=1)).strftime("%Y%m%d")+"_log.txt"

	time=np.array([])
	temp=np.array([])
	Vbias=np.array([])
	Vleak=np.array([])

	if os.path.exists(directoryName+fileNameYesterday):
		#######################
		#Exract the log info
		#######################
		x1=pd.read_csv(directoryName+fileNameYesterday,skiprows=0,delimiter='\t',na_values=('#DIV/0!',''))

		time=np.append(time,np.array(x1["time [s]"]))
		temp=np.append(temp,np.array(x1["H35_Tplot [K]"]))
		Vbias=np.append(Vbias,np.array(x1["HP 3478A [V]"]))
		Vleak=np.append(Vleak,np.array(x1["Keithley 617 [V]"]))

	if os.path.exists(directoryName+fileNameToday):
		#######################
		#Exract the log info
		#######################
		x1=pd.read_csv(directoryName+fileNameToday,skiprows=0,delimiter='\t',na_values=('#DIV/0!',''))

		time=np.append(time,np.array(x1["time [s]"]))
		temp=np.append(temp,np.array(x1["H35_Tplot [K]"]))
		Vbias=np.append(Vbias,np.array(x1["HP 3478A [V]"]))
		Vleak=np.append(Vleak,np.array(x1["Keithley 617 [V]"]))

	if len(time)==0:
		sys.exit()

	#Set garbage values to 0
	#These occur when changing thermometers
	temp=np.array([ max(0.0,i) for i in temp])
	
	#######################
	#Make the plots
	#######################

	#plt.ion()#interactive plotting so we can view fits in real time
	fig1=plt.figure(1)

	lastTime=time[-1]#Most recent logged time
	i12prior=bisect.bisect(time,lastTime-12*3600) #index 12 hours prior
	i2prior=bisect.bisect(time,lastTime-2*3600) #index 2 hours prior

	#TODO convert to human readable time
	#Understand saved timestamp
	#Dispay last data time, time of plot creation, and current values
	nowStr=datetime.now().strftime("%Y-%m-%d %H:%M")
	lastTimeStr=(datetime.fromtimestamp(lastTime)).strftime("%Y-%m-%d %H:%M")


	#Convert to appropriate units
	time=(time-lastTime)/3600 # [hrs ago]
	temp=temp*1000 # [mK]
	Vleak=Vleak*1000 # [mV]

	left=0.05
	top=0.95

	#Last 2 hours
	plt.clf()
	plt.plot(time[i2prior:],temp[i2prior:])
	plt.xlabel('time [hr]')
	plt.ylabel('tower temp [mK]')
	ax1=plt.gca()
	ax1.get_yaxis().get_major_formatter().set_useOffset(False)
	ax1.text(left, top, 'Plot Generated: '+nowStr+'\n'+'Last Data: '+str(temp[-1])+' mK\nat '+lastTimeStr,
	        horizontalalignment='left',
	        verticalalignment='top',
	        transform=ax1.transAxes)
	
	fig1.savefig("temp_v_time_2hr.png")

	plt.clf()
	plt.plot(time[i2prior:],Vbias[i2prior:],'r-')
	ax1=plt.gca()
	ax1.get_yaxis().get_major_formatter().set_useOffset(False)
	ax1.set_xlabel('time [hr]')
	ax1.set_ylabel('V_bias [V]', color='r')
	ax1.tick_params('y', colors='r')
	ax2=ax1.twinx()
	ax2.get_yaxis().get_major_formatter().set_useOffset(False)
	ax2.plot(time[i2prior:],Vleak[i2prior:],'b-')
	ax2.set_ylabel('V_leak [mV]', color='b')
	ax2.tick_params('y', colors='b')	
	
	ax1.text(left, top, 'Plot Generated: '+nowStr+'\n'+'Last Data: '+str(Vbias[-1])+' V\n'+str(Vleak[-1])+' mV\nat '+lastTimeStr,
	        horizontalalignment='left',
	        verticalalignment='top',
	        transform=ax1.transAxes)
	
	fig1.savefig("bias_v_time_2hr.png")

	#Last 12 hours
	plt.clf()
	plt.plot(time[i12prior:],temp[i12prior:])
	ax1=plt.gca()
        ax1.get_yaxis().get_major_formatter().set_useOffset(False)
	plt.xlabel('time [hr]')
	plt.ylabel('tower temp [mK]')
	fig1.savefig("temp_v_time_12hr.png")

	plt.clf()
	plt.plot(time[i12prior:],Vbias[i12prior:],'r-')
	ax1=plt.gca()
        ax1.get_yaxis().get_major_formatter().set_useOffset(False)
	ax1.set_xlabel('time [hr]')
	ax1.set_ylabel('V_bias [V]', color='r')
	ax1.tick_params('y', colors='r')
	ax2=ax1.twinx()
	ax2.plot(time[i12prior:],Vleak[i12prior:],'b-')
	ax2.set_ylabel('V_leak [mV]', color='b')
	ax2.tick_params('y', colors='b')	
	fig1.savefig("bias_v_time_12hr.png")


	
	
	
	#Copy to web page
	print subprocess.Popen("cp bias_v_time*.png /home/webusers/cdms/public_html/cdms_restricted/K100/thermometers/tempMon/images", shell=True, stdout=subprocess.PIPE).stdout.read()
	print subprocess.Popen("cp temp_v_time*.png /home/webusers/cdms/public_html/cdms_restricted/K100/thermometers/tempMon/images", shell=True, stdout=subprocess.PIPE).stdout.read()

	#try:
	#	input("Press enter to continue")
	#except SyntaxError:
	#	pass
