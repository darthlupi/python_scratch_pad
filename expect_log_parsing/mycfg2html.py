#!/usr/bin/python
import MySQLdb as mdb
import os, sys, csv



class MySqlCon:
        def __init__(self ,dbhost, dbuser, dbpass, dbdatabase ):
                try:
                    self.con = mdb.connect(dbhost, dbuser, dbpass, dbdatabase );
                    self.cur = self.con.cursor()
                except mdb.Error, e:
                    print "Error %d: %s" % (e.args[0],e.args[1])
                    sys.exit(1)
        def execsql(self,sql):
                self.cur.execute(sql)
        def returnone(self):
                return self.cur.fetchone()

                

def main ():

    mydb = MySqlCon('localhost','admin','admin','network_mess')
    #Recurse one level in the directory specified get the file names and extention...
    path="/var/www/html/cfg2html/"
    dir_list=os.listdir(path)
    old_line = ''

    start_route = 0;

    truncate = "truncate table host_interfaces;"
    try:
            mydb.execsql( truncate )
            next_id = mydb.returnone()
    except Exception, e:
            print str(e)
            sys.exit

    truncate = "truncate table host_routes;"
    try:
            mydb.execsql( truncate )
            next_id = mydb.returnone()
    except Exception, e:
            print str(e)
            sys.exit
    
    for fname in dir_list:
            dir_list2=os.listdir(path+fname)
            for sub_fname in dir_list2:
                    sub_f, sub_ext = os.path.splitext(sub_fname)
                    #If the extention indicate html we know we have the right file to start parseing!
                    #Open that sucker up and get to work parsing interface and route info!
                    if sub_ext == '.html':
                            print sub_f + sub_ext
                            open_file = open(path+fname+'/'+sub_fname, 'r')

                            #Set server specific information here.

                            print sub_f + "'s Network Config"
                            get_next_sql = "select IFNULL(max(id),-1) + 1 from host_interfaces;"
                            try:
                                mydb.execsql( get_next_sql )
                                next_id = mydb.returnone()
                            except Exception, e:
                                print str(e)
                                sys.exit
                            print 'Host id = ' + str(next_id[0]);

                            #All individual interface and route information goes here                            
                            for line in open_file:
                                    
                                #Get the interface info
                                if line.strip().startswith('inet addr:'):
                                        #Create get rid of pesky : and turn it into white spaces so we can do consistent splits
                                        int_config = line.replace(':',' ').split()
                                        int_name =  old_line.split()
                                        try:
                                                print int_name[0].strip('<PRE>') + ' ' + int_config[2] + ' ' + int_config[6]
                                                values = "'" + str(next_id[0]) + "','" + sub_f + "','" + int_name[0].strip('<PRE>') + "','" + int_config[2] + "','" + int_config[6] + "'" 
                                                
                                                insert_sql = "insert into host_interfaces ( id,hostname, interface, ip_address, netmask ) values ( " + values + ");"
                                                print insert_sql
                                                mydb.execsql( insert_sql )
                                        except Exception, e:
                                                print str(e)
                                #Get route info
                                if line.startswith('<A'):
                                                   start_route = 0
                                if start_route == 1:
                                        try:
                                                route = line.split()
                                                values = "'" + str(next_id[0]) +"','" + sub_f + "','" + route[0] + "','" + route[1] + "','" + route[2] + "','" + route[7].strip('</PRE>') + "'"
                                                insert_sql = "insert into host_routes ( id,hostname, dest_ip,gate_ip,mask_ip,interface ) values ( " + values + ");"
                                                print insert_sql
                                                mydb.execsql(insert_sql)
                                        except Exception, e:
                                                print str(e)
                                if line.startswith('Destination     Gateway'):
                                                   start_route = 1                                        
 
                                                   
                                old_line = line
                            open_file.close

                    

   


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e)
        #traceback.print_exc()
        os._exit(1)





