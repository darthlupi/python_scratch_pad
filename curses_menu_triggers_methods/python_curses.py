#!/usr/bin/python
import sys, optparse, datetime, curses                                                                
from curses import panel 
from shutil import copyfile

def exit_clean():
    print_stuff()
    sys.exit(0)
def print_stuff():
        print "\nCaptured ctrl+c!"
		

class Menu(object):                                                          

    def __init__(self, items, stdscreen):                                    
        self.window = stdscreen.subwin(0,0)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                

        self.position = 0                                                    
        self.items = items                                                   
        self.items.append(('exit','exit'))                                   

    def navigate(self, n):                                                   
        self.position += n                                                   
        if self.position < 0:                                                
            self.position = 0                                                
        elif self.position >= len(self.items):                               
            self.position = len(self.items)-1                                
    def clear_screen():
        self.window.clear()

    def display(self):                                                       
        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  

        while True:                                                          
            self.window.clear()
            self.window.refresh()                                            
            curses.doupdate()                                                
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                msg = '%s' % item[0] + item[1]                            
                self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:                         
                if self.position == len(self.items)-1:                       
                    break                                                    
                else:                                                        
                    self.items[self.position][2](self.items[self.position][3])                           
            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
		
class CreateInventory(object):
    def __init__(self,menu):
        #The strings to replace to setup your appserver.  These values should exist in the inventory.
        self.DEFAULT_APPSERVER_FQDN = "appserver01.domain.local"
        self.DEFAULT_APPSERVER_IP = "10.10.10.10"
        self.DEFAULT_APPSERVER_NODE = "NODE1"

        self.DEFAULT_MAPSERVER_FQDN = "mapserver01.domain.local"
        self.DEFAULT_MAPSERVER_IP = "10.10.10.10"

        #The inventory template that will be copied.  
        #This would be a good argument to pass in.
        self.src_inventory = "/etc/ansible/inventories/templates/two_server_template"
        self.appserver_servers = {
            'appserver_1':{'fqdn':"appserver3000.domain.local",'ip':"10.10.10.10",'node':"Helmond", }
        }
        self.mapserver_servers = {
            'mapserver_1':{ 'fqdn':"",'ip':"", }
        }
        self.menu = menu
        self.set_menu_items()
    def set_field(self,field):
        self.appserver_servers['appserver_1']['fqdn'] = "BLANKOOOOOPER"
        self.set_menu_items()        
    def set_menu_items(self):
        #Set the menu items
        #(Display text 1,display text 2 ( concat with 1 ) , function to call,paramter for function if needed )
        self.items = [
                ('App Server Hostname: ',  self.appserver_servers['appserver_1']['fqdn'], self.set_field,0 ),
                ('  App Server IP: ',self.appserver_servers['appserver_1']['ip'],  self.set_field,1 ),
                ('  App Server Node Name: ',self.appserver_servers['appserver_1']['node'], self.set_field,2 ),
                ('MAPSERVER  Node Hostname: ',self.mapserver_servers['mapserver_1']['fqdn'],self.set_field,3 ),
                ('  MAPSERVER Node IP Address: ',self.mapserver_servers['mapserver_1']['ip'], self.set_field,4 ),
                ('Save and Quit','', self.save_and_quit ),
                ('Quit','', quit ),
                ]
        #Update the menu with any new items.
        self.menu.items = self.items 
    def save_and_quit(self):
        dest = "/tmp/my_inventory_"# + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        #Create a copy of the template that we can edit.
        copyfile(self.src_inventory, dest)
        #Edit the inventory file replace all of the required values.
        with open(self.src_inventory) as infile, open(dest, 'w') as outfile:
            for line in infile:
                #Replace default appserver hostname, IP and node with the values you set in the appserver_servers dictionary.
                line = line.replace(self.DEFAULT_APPSERVER_FQDN, self.appserver_servers['appserver_1']['fqdn'])
                line = line.replace(self.DEFAULT_APPSERVER_IP, self.appserver_servers['appserver_1']['ip'])
                line = line.replace(self.DEFAULT_APPSERVER_NODE, self.appserver_servers['appserver_1']['node'])
                #Replace default MAPSERVER hostname and IP with the values you set in the mapserver_servers dictionary.
                line = line.replace(self.DEFAULT_MAPSERVER_FQDN, self.mapserver_servers['mapserver_1']['fqdn'])
                line = line.replace(self.DEFAULT_MAPSERVER_IP, self.mapserver_servers['mapserver_1']['ip'])

                #Replace the 
                outfile.write(line)
        print "Created new inventory file: " + dest
        quit()
        
class InventoryEditor(object):
        def __init__(self, stdscreen):                                           
            self.screen = stdscreen                                              
            curses.curs_set(0)                                                   
            submenu_items = [                                                    
                    ('beep', curses.beep),                                       
                    ('flash', curses.flash)                                      
                    ]                                                            
            submenu = Menu(submenu_items, self.screen)                           
            main_menu = Menu([], self.screen)                       
            my_inventory = CreateInventory(main_menu)
            main_menu.display()

if __name__ == '__main__':
    try:
        curses.wrapper(InventoryEditor)
    except KeyboardInterrupt:
        pass
        my_parser = exit_clean()

