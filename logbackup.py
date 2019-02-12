#A few lines of code to grab the auotomatically generated k100 time,bias log and back it up on chocula


###############################################################################
# this is the standard boilerplate that allows this to be run from the command line
###############################################################################
if __name__ == '__main__':

	from datetime import datetime,timedelta
	import subprocess

	#Get the filenames
	pathFrom="i/K100/"
	pathTo="/data/chocula/k100/k100_log/"
	fileToday=datetime.now().strftime("%Y%m%d")+"_log.txt"
	fileYesterday=(datetime.now() - timedelta(days=1)).strftime("%Y%m%d")+"_log.txt"
	
	print subprocess.Popen("sftp Administrator@vuk-01:"+pathFrom+fileToday+" "+pathTo, shell=True, stdout=subprocess.PIPE).stdout.read()
	print subprocess.Popen("sftp Administrator@vuk-01:"+pathFrom+fileYesterday+" "+pathTo, shell=True, stdout=subprocess.PIPE).stdout.read()
