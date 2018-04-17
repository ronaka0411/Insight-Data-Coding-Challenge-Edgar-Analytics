
#!/usr/bin/python

####################################################################################################
# Title : Sorurce code for Insight Data Engineering Fellowship Coding Challenge April 2018         #
# Author: Ronak Agrawal (Graduate Engineering Assistant, CS Graduate Student, NJIT, NJ             #
# Input : log.csv file which contains weblogs from SEC's EDGAR system                              #
#         inactivity_period.txt which contains single value to identify when a session is over.    #
# Output: sessionization.txt with details regarding each user session which includes               #
#         User IP Address, duration of session and number of documents requested during the session#
####################################################################################################

import sys
import datetime

'''
This method writes the sessions created and stored in a list to the output file with append permissions.
'''

def write_output():
    global out_session
    with open(output_file,'a') as out: # Opening output file with append permissions
        for ip in out_session:
            output_string=ip[0]+','+ip[1].strftime('%Y-%m-%d %H:%M:%S')+','+ip[2].strftime('%Y-%m-%d %H:%M:%S')+','+str(ip[3])+","+str(ip[4])+"\n" #strftime converts the struct_time object to the format given in the argument
            out.write(output_string)
    out_session=[] # clear the out sessions once written to the file to avoid over lapping of sessions
'''
This method checks for users who exceeded inactivity period and thus creates a session. All the sessions are stored in a list. The method to write these sessions to putput file is called. 
'''
def check_inactive(base_time,inactive_time):

    global active_session
    expired_ips=[]
    
    for ip in range(len(active_session)):
        time_elapse = base_time - active_session[ip][2]
        if time_elapse.total_seconds() > inactive_time:
            duration = active_session[ip][2] - active_session[ip][1]
            out_session.append([active_session[ip][0],active_session[ip][1],active_session[ip][2],int(duration.total_seconds())+1,active_session[ip][3]])
            expired_ips.append(ip)
            
    expired_ips.sort(reverse=True) # Here we arrange it in decending order because we are deleting each active session and thus reducing the size of that list.
    
    for ip in expired_ips: # if expired_ips not sorted decending order then throws error, because index of loop is increasing and active session length is reducing, throws list index out of bound error
        del active_session[ip]
        
    write_output() # write the expired_ip users sessions to the output file
         
'''
To convert the given format of date and time into a time_struct format to calculate seconds using various datetime methods
'''
def time_conversion(date_value,time_value):
    try:
        return datetime.datetime.strptime(date_value+' '+time_value,'%Y-%m-%d %H:%M:%S') 
    except ValueError:
        print('Value Error in time values')
        sys.exit(1)

'''
This method read in the input .csv file line by line
splits each line with comma as delimeter
and prepares a active session list
For each new line, it checks if the user IP is already in the list (updates the number of docs requested) or its a new IP (appends to the list)
Also iteratively it checks for each new time value in the new line, using the check_inactive() method is the time difference between start time and base time exceeds the inactivity period or not
At last it checks for the current system time value using check_inactive() method where we get all the sessions which we created regardless of inactivity period.
'''
def sessionize(filename,inactive_time):
    header_index = {}
    file_header = True                                        #Assuming that the first line (row/observation) of the input file is always header of different fields of the file
    '''
    Start reading the input file line by line
    '''
    with open(filename,'r') as f:
        for line in f:
            if file_header:             
                header = line.split(',')
                for field in header:
                    header_index[field] = header.index(field) # to determine at what place the particular field is in the input field assuming constant nomenclature of fields
                file_header = False
                # print(header_index)
            else:
                record = line.split(',')
                request_time = time_conversion(record[header_index['date']],record[header_index['time']]) # Convert the date and time values into struct_time format using datetime
                
                # Check and Remove the expired user IPs from active sessions This is based on the inactive period.
                # If any user in active IP list has surpassed this period then should be removed from active list and a session should be made wriitern to output file
                check_inactive(request_time,inactive_time)
                
                Flag = False
                for ip in range(len(active_session)):       # This is to check if we already have the IP in the active_sessions list
                    if active_session[ip][0] == record[0]:  # Once we find the IP is already there in the list we update the time for that IP by using flag and assignment statements
                        Flag = True
                        break                               # Once we find the IP, get out of the for loop.
                if Flag == True:
                    active_session[ip][2]=request_time      # update the request time for that user IP
                    active_session[ip][3]+=1                # increment number of document requested
                else:
                    active_session.append([record[0],request_time,request_time,1])
                        
    check_inactive(datetime.datetime.now(),inactive_time)   # After the end of file is reached check all the active sessions based on the current system time
                                                            # Create new sessions regardless of inactive time
            
            
'''
The main function takes the input arguments and passes it to local variable which are then sent to sessionize function where they are processed.
'''

def main():

    args = sys.argv[1:]                 # Exclude the first command line argument which is the file name itself and collect other arguments in a List

    if not args:                        # Check if inout file and output filenames are passed as argument correctly
        print ('usage: .csvfilename inactivity_period.txt sessionization.txt')
        sys.exit(1)

    filename = args[0]                  # Take the input filename into a local variable
    inactive_period_file = args[1]

    with open(inactive_period_file,'r') as inactive:
        for line in inactive:
            inactivity_period = int(line)
     
    sessionize(filename,inactivity_period)
    print('Sessionization in process...')
    print('Done! Please check the output file for all the user sessions.')

'''
Start of the program
'''
# Declaring global variables for this application
# Important: Here we cannot use Dictionary data structure as it will complicate the order in which we want the output
# Thus lets use a 2D array, List of lists
active_session = []             # Array of active session with each element array of structure [IP,StartTime,RequestTime,NoOfDocsRequested]
out_session = []                # Array of expired sessions which needs to be written on output file with the following structure [IP,StartTime,RequestTime,Duration,NoOfDocsRequested]
output_file = sys.argv[3]       # Taking the third command line argument as the output file. Be assured the file exists in the folder specified

# We need to clear the output file before writting or appending anything to it.
with open(output_file,'w') as out:
    print('Output file cleared, ready for writting new content...')
# Use of __name__ variable to initiate main method
if __name__ == '__main__':
    main()
