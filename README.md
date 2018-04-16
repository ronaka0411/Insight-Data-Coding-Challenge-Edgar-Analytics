# Insight-Data-Coding-Challenge-Edgar-Analytics
Real time data streaming, analysis and viewing, related to time and number of documents requested by a user on SEC's EDGAR system.

# Objective
The SEC maintains EDGAR weblogs showing which IP addresses have accessed which documents for what company, and at what day and time this occurred. The objective of this streaming data analysis approach is to provide a real-time view into how users are accessing EDGAR, including how long they stay and the number of documents they access during the visit.

# Summary
As a data engineer, the main role for this activity is to work on the streaming data pipeline, perform some analysis and hand over the information to the front-end development team.

# Details
## 1. Input
We have two input files. One is log.csv which contains all the requests with each line representing a single request with format as follows: ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser. Anpther input file is inactivity_period.txt which contains the number of seconds after which a user session is ended, that is a default(threshold) value for a session to end.

## 2. Output
We need to list out each session with following information: ip, session_start_time, session_end_time, duration_of_session, number_of_documents_requested. The key part here to analyse is the time.

## 3. Language
Here I have used python 3 to develop this application. Each line is explained with proper flow and comments. As a recent grad the code may look a bit obvious about few things, but this will help all the beginners as well, to understand the code.

## 4. Implementation
The program reads in the .csv file line by line and to ignore the first line which is assumed to be the header field, I have implemented flags. We can always use the index of each column from this operation. The program reads the input file inactivity_period and stores the value of inactivity_period. Here I have converted the date and time values in each line/field of the .csv file into struct_time using datetime function, which basically gives a tuple of all the date and time values together in the format specified in the argument of datetime function. This can be useful in further process. The major role played by defining local and global variables for this activity, and to know the scope of each variable while each line is executed in the code. 
Here the sessions are created when following two events occur:
1. When the user requests for the time greater than inactivity period the sessionizer, creates a session whose duration will be equal to inactivity period. 
2. When we reach at the end of the file, all the user IPs are sessionized irrespective of the inactivity period, here the duration of the session can be more than the inactivity period. 

## 5. Difficulties
The first challenge here was to decide the data structure for the output data. Here each session written to output file is first based on the order in which it is created and if simultaneously more sessions are created then the order is based on the order in which they appear in the input file. I had first started with making a dictionary of each active and expired user (session). But with that I had to sort the dict keys based on the order they were created. Here the order of session is important as well. Thus is would become much complicated. So then I used a list of lists which is basically a 2D array. Here the order is intact and the deletion of active sessions is also easier process.




