#Nick Mast
#Sept 2017

###############################################################################
#fridgeTempPlotter
#
# A script to retrieve and display K100 temperature log data
###############################################################################

###############################################################################
# this is the standard boilerplate that allows this to be run from the command line
###############################################################################
if __name__ == '__main__':
	import sys
	import subprocess
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	import numpy as np
	
	#Plot the most recent n minutes of data
	#Assumes temperature is recorded every 6 sec
	#numEntries=int(sys.argv[1])*10

	#Make a local copy of the logfile from vuk-01
	print subprocess.Popen("sftp Administrator@vuk-01:i/K100/temperature_20171020.txt TempLog.txt", shell=True, stdout=subprocess.PIPE).stdout.read()
	
	#Exract the time and temperature info
	time=[]
	temp=[]
	file=open("TempLog.txt","r")
	lines=file.readlines()
	#numEntries=min(numEntries,len(lines))
	for line in lines[7:]:
		time.append(float(line.split()[0]))
		temp.append(float(line.split()[2]))


	time=np.array(time)
	temp=np.array(temp)
	
	#Set garbage values to 0
	#These occur when changing thermometers
	temp=np.array([ max(0.0,i) for i in temp])
	
	#Change to minutes from most recent value
	#latest=time[-1]
	#time=(time-latest)/60
	
	#Change to daily time in hours and temp in mK
	time=(time/3600)%24
	temp=temp*1000

	#plt.ion()#interactive plotting so we can view fits in real time
	fig1=plt.figure(1)

	dt=6#6 seconds per sample
	
	numEntries=int(1*60/dt)# 1 min
	plt.plot(time[-numEntries:],temp[-numEntries:])
	plt.xlabel('time [hr]')
	plt.ylabel('tower temp [mK]')
	fig1.savefig("temp_v_time_1min.png")
	
	numEntries=int(5*60/dt)# 5 min
	plt.plot(time[-numEntries:],temp[-numEntries:])
	fig1.savefig("temp_v_time_5min.png")
	
	numEntries=int(30*60/dt)# 30 min
	plt.plot(time[-numEntries:],temp[-numEntries:])
	fig1.savefig("temp_v_time_30min.png")

	numEntries=int(2*60*60/dt)# 2 hour
	plt.plot(time[-numEntries:],temp[-numEntries:])
	fig1.savefig("temp_v_time_2hr.png")

	numEntries=int(12*60*60/dt)# 12 hour
	plt.plot(time[-numEntries:],temp[-numEntries:])
	fig1.savefig("temp_v_time_12hr.png")
	
	#Copy to web page
	print subprocess.Popen("cp temp_v_time*.png /home/webusers/cdms/public_html/cdms_restricted/K100/thermometers/tempMon/images", shell=True, stdout=subprocess.PIPE).stdout.read()

	#try:
	#	input("Press enter to continue")
	#except SyntaxError:
	#	pass
