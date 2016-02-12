#!/usr/bin/python
import MySQLdb
import json
import copy
import sys

"""
Purpose:  This script will all you to manage a database backed Ansible Inventory.
It will also generate json output to allow you to query against it.
Written by: Robert Lupinek ??/??/2014
Version: 1.0
Reference Docs: http://docs.ansible.com/developing_inventory.html
"""

#I need to create the real scripts to create z tables!
#create table hosts ( host_id int, host_name varchar(99), status varchar(24) );
#create table groups ( group_id, group_name, status varchar(24) );
#create table grouped_hosts ( group_id, host_id );
#create table group_variables ( variable_id, group_id,variable );

#A little class to help with any our mysql needs.  Right now it is a LITTLE redundant
class MySQLTools:
  def __init__(self,host,user,passwd,db):
	try:
  	self.db = MySQLdb.connect(host="localhost",user="admin",passwd="admin",db="ansible_inventory")
	except Exception, e:
  	print repr(e)
  	sys.exit()
  def do_query(self,query):
	try:
  	cur = self.db.cursor()
  	cur.execute(query)
  	return cur.fetchall()
	except Exception, e:
  	print repr(e)
  	sys.exit()

def arg_check(provided,expected):
  if provided != expected:
	print "Wrong number of arguments..."
	help()
	sys.exit()


def add_host(db,args):
  arg_check(len(args),3)
  results = db.do_query('insert into hosts ( host_name, status ) VALUES ("' + args[2].lower() + '", "active");')

def add_group(db,args):
  arg_check(len(args),3)
  results = db.do_query('insert into groups ( group_name, status ) VALUES ("' + args[2].lower() + '", "active");')

def add_host_to_group(db,args):
  arg_check(len(args),4)
  group_name = str(args[3])
  host_name = str(args[2])
  results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
  for id in results:
	group_id = id[0]
  results = db.do_query('select host_id from hosts where host_name ="' + host_name  + '";')
  for id in results:
	host_id = id[0]
  #Make sure the required variables are set.  This will also make sure the group and host exist as you specified.
  try:
	group_id
  except NameError:
	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
	sys.exit()
  try:
	host_id
  except NameError:
	print "Host was not found.  You may need to add the host " + host_name + " before running this command."
	sys.exit()
  #Add the host to the group.
  query = 'insert into grouped_hosts ( group_id, host_id ) VALUES ( "' + str(group_id) + '","' + str(host_id) + '");'
  results = db.do_query(query)

  print "Added host: " + host_name + " to group: " + group_name + "."


def set_group_vars(db,args):
  arg_check(len(args),5)
  group_name = str(args[2])
  variable = str(args[3])
  value = str(args[4])

  results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
  for id in results:
	group_id = str(id[0])

  #Make sure the required variables are set.  This will also make sure the group exists.
  try:
	group_id
  except NameError:
	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
	sys.exit()

  results = db.do_query( 'select group_id from group_variables where group_id ="' + group_id  + '" and variable = "' + variable + '";' )

  #Add the variable to the group.
  query = 'insert into group_variables ( group_id, variable, value ) VALUES ( "' + group_id + '","' + variable.lower() + '", "' + value + '") ON DUPLICATE KEY UPDATE value=VALUES(value) ;'
  results = db.do_query(query)
  print "Variable: " + variable.lower() + " set to value: " + value + " for the group " + group_name + "."



def del_host(db,args):
  arg_check(len(args),3)
  host_name = str(args[2])
  results = db.do_query('select host_id from hosts where host_name ="' + host_name  + '";')
  for id in results:
	host_id = str(id[0])
  #Make sure the required variables are set.  This will also make sure the host exists as you specified.
  try:
	host_id
  except NameError:
	print "Host was not found.  You may need to add the host " + host_name + " before running this command."
	sys.exit()

  results = db.do_query('delete from grouped_hosts where host_id ="' + host_id  + '";')
  results = db.do_query('delete from hosts where host_id ="' + host_id  + '";')
  print "Host was deleted from all groups and removed from inventory."

def del_group(db,args):
  arg_check(len(args),3)
  group_name = str(args[2])
  results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
  for id in results:
	group_id = str(id[0])
  #Make sure the required variables are set.  This will also make sure the group exists as you specified.
  try:
	group_id
  except NameError:
	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
	sys.exit()
  results = db.do_query('delete from grouped_hosts where group_id ="' + group_id  + '";')
  results = db.do_query('delete from group_variables where group_id ="' + group_id  + '";')
  results = db.do_query('delete from groups where group_id ="' + group_id  + '";')
  print "Group was deleted and removed from inventory."


def del_host_from_group(db,args):
  arg_check(len(args),4)
  group_name = str(args[3])
  host_name = str(args[2])
  results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
  for id in results:
	group_id = id[0]
  results = db.do_query('select host_id from hosts where host_name ="' + host_name  + '";')
  for id in results:
	host_id = id[0]
  #Make sure the required variables are set.  This will also make sure the group and host exist as you specified.
  try:
	group_id
  except NameError:
	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
	sys.exit()
  try:
	host_id
  except NameError:
	print "Host was not found.  You may need to add the host " + host_name + " before running this command."
	sys.exit()
  #Delete the host from the group.
  query = 'delete from grouped_hosts where group_id = "' + str(group_id) + '" and host_id = "' + str(host_id) + '";'
  results = db.do_query(query)
  print "Deleted host: " + host_name + " from group: " + group_name + "."


def del_group_vars(db,args):

  arg_check(len(args),4)
  group_name = str(args[2])
  variable = str(args[3])

  results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
  for id in results:
	group_id = str(id[0])
  #Make sure the required variables are set.  This will also make sure the group exists.
  try:
	group_id
  except NameError:
	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
	sys.exit()

  results = db.do_query('select variable from group_variables where group_id ="' + group_id  + '" and variable = "' + variable + '";')
  for id in results:
	test = str(id[0])
  #Make sure the required variables are set.  This will also make sure the host exists as you specified.
  try:
	test
  except NameError:
	print "Variable was not set for this group.  You may need to add the variable " + variable + " to the group " + group_name + " before running this command."
	sys.exit()

  query = 'delete from group_variables where group_id = "' + str(group_id) + '" and variable = "' + variable + '";'
  results = db.do_query(query)
  print "Deleted variable: " + variable + " from group: " + group_name + "."

def display_host(db,args):
  if len(args) == 3:
	host_name = str(args[2])
	results = db.do_query('select host_id from hosts where host_name ="' + host_name  + '";')
	for id in results:
  	host_id = str(id[0])
	#Make sure the required variables are set.  This will also make sure the host exists as you specified.
	try:
  	host_id
	except NameError:
  	print "Host was not found.  You may need to add the host " + host_name + " before running this command."
  	sys.exit()

	print "Hostname:\n  hostname: " + host_name
	results = db.do_query('select g.group_name from grouped_hosts gh, groups g where gh.group_id = g.group_id and gh.host_id = "' + host_id + '";')
	print "Groups host is a member of:"
	for row in results:
  	print "  group name: " + row[0]
  else:
	results = db.do_query('select host_name from hosts;')
	print "ALL HOSTS:"
	for row in results:
  	print "  hostname: " + row[0]

def display_group(db,args):
  if len(args) == 3:
	group_name = str(args[2])
	results = db.do_query('select group_id from groups where group_name ="' + group_name  + '";')
	for id in results:
  	group_id = str(id[0])
	#Make sure the required variables are set.  This will also make sure the host exists as you specified.
	try:
  	group_id
	except NameError:
  	print "Group was not found.  You may need to add the group " + group_name + " before running this command."
  	sys.exit()
	print "Group name:\n  group name:" + group_name
	results = db.do_query('select h.host_name from grouped_hosts gh, hosts h where gh.group_id = h.host_id and gh.group_id = "' + group_id + '";')
	print "Member hosts:"
	for row in results:
  	print "  hostname: " + row[0]
	results = db.do_query('select g.group_name, v.variable, v.value from group_variables v, groups g where g.group_id = v.group_id and "' + group_id + '" group by g.group_name;')
	print "Variables:"
	for row in results:
  	print "  variable: " + row[1] + " = " + row[2]
  else:
	results = db.do_query('select group_name from groups;')
	print "ALL GROUPS:"
	for row in results:
  	print "  group name: " + row[0]

def display_vars(db,args):
  results = db.do_query('select g.group_name, v.variable, v.value from group_variables v, groups g where g.group_id = v.group_id group by g.group_name;')
  print "Variables:"
  for row in results:
	print "  group name: " + row[0] + " variable: " + row[1] + " = " + row[2]


def get_inventory(db):
  #This function pulls the dynamic ansible inventory from MySQL and outputs in json format.
  #See http://docs.ansible.com/developing_inventory.html to see what anisble requires for json output.

  groups_dict = {} #Main dictionary that contains the hosts disctionary and group variables dictionary
  sub_dict = {} #This dictionary is used as a place holder dictionary that we populate and reuse after copying it's contents into the groups_dict
  host_list = [] #Each group will need a list to contain the hosts associated with it.
  var_dict = {} #A dictionary that will contain any variables associated with the group.

  #Get a list of group ids and names
  group_results = db.do_query('SELECT group_id, group_name FROM groups where status = "active"')

  for row in group_results:
	group_id = row[0]
	group_name = row[1]

	#Clear the temporary dictionaries
	sub_dict.clear()
	var_dict.clear()

	#Select all hosts in the hosts table that are associated with the group we are currently looping through.
	query = 'select host_name from hosts where host_id in ( select host_id from grouped_hosts where group_id = "' + str(group_id) + '" ) AND status = "active";'
	host_results = db.do_query(query)
	#Clear the host_list list before we start appending to it.
	host_list = []
	#Loop through hosts and build a new list that will be added as 'hosts' to the dictionary
	for host_names in host_results:
  	host_list.append(host_names[0])
	sub_dict['hosts'] = host_list

	#Gather the group variables
	#Select all variables associated with the group we are looping through
	query = 'select variable, value from group_variables where group_id ="' + str(group_id) + '";'
	var_results = db.do_query(query)
	#Loop through variables and build a dictionary
	for var in var_results:
  	var_dict[var[0]] = var[1]
	sub_dict['vars'] = var_dict.copy()

	#Copy the contents of the sub_dict to the group dictionary
	groups_dict[group_name]=sub_dict.copy()

  #Convert output to json format and output to stdout
  groups_json = json.dumps(groups_dict)
  print groups_json




def help():
  print "The script is used to manipulate and pull inventory for use with ansible."
  print "\n--Export--"
  print "To export inventory for ansible run\n   ansible_inventory.py"
  print "\n--Add and set--"
  print "To add a host\n   ansible_inventory.py add_host host"
  print "To add a group\n   ansible_inventory.py add_group group"
  print "To add a host to a group\n   ansible_inventory.py add_host_to_group host group"
  print "To create or set a group variable\n   ansible_inventory.py set_group_vars group variable_name variable_value"
  print "\n--Delete--"
  print "To delete a host\n   ansible_inventory.py del_host host"
  print "To delete a group\n   ansible_inventory.py del_group group"
  print "To remove host from a group\n   ansible_inventory.py del_host_from_group host group"
  print "To delete group variables\n   ansible_inventory.py del_group_vars group variable_name"
  print "\n--Display--"
  print "To display all hosts\n   ansible_inventory.py display_host"
  print "To display specific hosts\n   ansible_inventory.py display_host host"
  print "To display all groups\n   ansible_inventory.py display_group"
  print "To display specific groups\n   ansible_inventory.py display_group group"
  print "To display all group variables\n   ansible_inventory.py display_vars"
  print "To display this help screen\n   ansible_inventory.py help"


def main():

  #This variable should only be set > 0 if an argument was provided a function was called.
  command_run = 0

  #Create a new MySQLTools object
  db = MySQLTools("localhost","admin","admin","ansible_inventory")

  #If no arguments are provided then
  if len(sys.argv) == 1 or sys.argv[1] == '--list':
	get_inventory(db)
	command_run = 1

  if len(sys.argv) > 1:
	#Adds and sets
	if sys.argv[1] == 'add_host':
  	add_host(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'add_group':
  	add_group(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'add_host_to_group':
  	add_host_to_group(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'set_group_vars':
  	set_group_vars(db,sys.argv)
  	command_run = 1

	#Deletes
	if sys.argv[1] == 'del_host':
  	del_host(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'del_group':
  	del_group(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'del_host_from_group':
  	del_host_from_group(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'del_group_vars':
  	del_group_vars(db,sys.argv)
  	command_run = 1

	#Displays
	if sys.argv[1] == 'display_host':
  	display_host(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'display_group':
  	display_group(db,sys.argv)
  	command_run = 1
	if sys.argv[1] == 'display_vars':
  	display_vars(db,sys.argv)
  	command_run = 1


	#If any parameters were provided that we aren't expecting then print the help.
	#Also, print help if you used the help argument
	if command_run == 0 or sys.argv[1] == 'help':
  	help()

if __name__ == "__main__":
	main()



