#!/usr/bin/python
import MySQLdb as mdb
import os, sys, csv, pexpect, re

####################################################################
#Script uses pexpect to poll the CS2K for PRI, Packet Cable, and
#SIP trunk utilization and capacity.  Also, script poplulates
#MySQL database designed to store capacity planning info.
#
#Creator: Robert Lupinek -- Created: 2/13/2012
#Modified by: Robert Lupinek -- Modified: 2/14/2012
####################################################################


##Simple MySQL class
class MySqlCon:
        def __init__(self ,dbhost, dbuser, dbpass, dbdatabase ):
                try:
                    self.con = mdb.connect(dbhost, dbuser, dbpass, dbdatabase );
                    self.cur = self.con.cursor()
                except mdb.Error, e:
                    print "Error %d: %s" % (e.args[0],e.args[1])
                    sys.exit(1)
        def execsql(self,sql):
                try:
                	self.cur.execute(sql)
		except Exception, e:
			print "sql fail..."
                        print str(e)                	
        def returnone(self):
                try:
                	return self.cur.fetchone()
		except Exception, e:
			print "sql fail..."
                        print str(e) 
        def returnall(self):
        	try:
                	return self.cur.fetchall()                        
		except Exception, e:
			print "sql fail..."
                        print str(e)                 

def main ():
	#INITIAL MySQL connection and return object...
	mydb = MySqlCon('localhost','user','password','tables')
	
	ssh_newkey = 'Are you sure you want to continue connecting'
	# my ssh command line
	
	p=pexpect.spawn('ssh user@host')
	
	expect_text = '';
	
	#p.logfile = sys.stdout

	i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
	if i==0:
    		p.sendline('yes')
    		i=p.expect([ssh_newkey,'Password:',pexpect.EOF])
    
	if i==1:
    		p.sendline("engineer1")
    		p.expect('Enter User Name')
    		expect_text += p.before
    		p.sendline("nepoll");
    
   		p.expect('Enter Password')
    		expect_text += p.before
    		p.sendline("engineer1")
    
    		p.expect('[^>]')
    		expect_text += p.before
    		p.sendline("soc;");
    
    		p.expect('>SOC:')
    		expect_text += p.before
    		p.sendline("select group cs2c; select group cs2b; select group mdc;")
    		
    		p.expect('[^>]')
    		expect_text += p.before
    		p.sendline("select group spms;")
    		
    		p.expect('[^>]')
    		expect_text += p.before
    		p.sendline("select group cs2n;")
    		
    		p.expect('[^>]')
    		expect_text += p.before
    		p.sendline("quit;")
    		
    		p.expect('>CI:')
    		expect_text += p.before
    		p.sendline("logout");
    		
    		p.expect(pexpect.EOF)
    		
    		#print expect_text; #UNCOMMENT TO DISPLAY WHAT IS BEING CAPTURED IN expect_text variable


    		####################################################################
    		#Now that we have the output from the switch, parse that junk...    
    		####################################################################
    		#Split the output from pexpect by newline to create rows of data    
    		row_data = '';
    		check_select = ''
    		insert_statement = ''
    		check_result = []
    		system_name = ''
    		
    		for expect_rows in expect_text.split('\n'):
			#I pondered regex ( re class ), split string, and finally settled on space delimted
			#Below I am generating the individual data columns
    			exp_id = expect_rows[0:4]
    			exp_name = expect_rows[10:33]
    			exp_current = expect_rows[40:48].strip()
   			exp_max = expect_rows[49:56].strip()
   			
   			#Sloppy column name verifier.  We only want to suck up particular columns ( should maybe be a search throuh list? )
    			if exp_id == 'MDC0' or exp_id == 'SPMS' or exp_id == 'CS2C' or exp_id == 'CS2B' or exp_id == 'CS2N':
    				row_data = exp_id + " | " + exp_name + " | " + exp_current  + " | " + exp_max + " | "	
    				print "Near raw expect data: " + row_data
    				exp_name = exp_name.rstrip(' ') #Clean up the system names
    				
    				#Check to see if the system exists.  First build and then print select statement.
    				check_select = "select system_name, system_id from systems where system_name = '" + exp_id + "- " + exp_name + "';"
    				print check_select
    				
				mydb.execsql( check_select )
				check_result = mydb.returnone()

    				
    				if check_result:   #If there is a result, the system exists.
    					#Start adding capacity details under the existing system name
    					print "System exists, so just add details"
    					print check_result[0] + ' id='+ str(check_result[1])    #Print out the named and id of system
    					#Build the insert statement for details
					insert_statement = "insert into capacity_data (system_id, cap_name,int_data1,int_data2,date1) values ( '" + str(check_result[1]) + "','"+ exp_name + "','" + exp_current + "' , '" + exp_max +"', now() );"
					mydb.execsql( insert_statement )
					print insert_statement    					
    				else:		  #Apparently the system doesn't exist... ...Create and add the current record for the system
    					#Insert system and capacity details
    					print "System not found.  System AND details must be added..."
    					insert_statement = "insert into systems (system_name,system_description, modify_date, create_date ) values ( '" + exp_id + "- " + exp_name + "','" + exp_name + "',now(), now() );"
    					
    					print insert_statement
    					print check_select

					mydb.execsql( insert_statement )
					
					#Rerun the select statement checking to see if the new system_name has been inserted successfully thus retrieving the appropriate system_id
					mydb.execsql( check_select )
					check_result = mydb.returnone()
					
					#Insert the details :)
					if check_result:
						print "insert details for: " + check_result[0]  + " " + " id=" + str(check_result[1])
						insert_statement = "insert into capacity_data (system_id, cap_name,int_data1,int_data2,date1) values ( '" + str(check_result[1]) + "','"+ exp_name + "','" + exp_current + "' , '" + exp_max +"', now() );"
						mydb.execsql( insert_statement )
						print insert_statement
					else:
						print "Make sure the insert didn't fail for the new system.  Doing a select on it's named returned nothing for some reason."
					
					
    					
				    
	elif i==2:
    		print "I either got key or connection timeout"
    		pass
	#print p.before # print out the result
    
if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e)
        #traceback.print_exc()
        os._exit(1)