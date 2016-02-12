#!/usr/bin/python
import vmware_helper
#To use command line ags
#Results in an object example to use: args.password
#args = get_args()

host = 'vcenterhost.com'
user = 'user'
pwd = 'password'
port = 443
vm_name = 'test.vm'

uuid = '501b6f99-3dc7-fda3-9741-1fa115d56ea1' #Instance UUID
vm_helper = vmware_helper.vmware_helper(host,user,pwd,port)
#vm = vm_helper.get_vm(uuid,'uuid')
vm = vm_helper.get_vm(vm_name,'name')
vm = vm_helper.annotate_vm(vm,'THIS IS SO AWESOME!')
#vm_helper.configure_vm(vm,2,4096,"You rule bro!")
#vm_helper.power_state(vm,'on')
