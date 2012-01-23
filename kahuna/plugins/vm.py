#!/usr/bin/env jython

from optparse import OptionParser

from kahuna.session import ContextLoader
from org.jclouds.abiquo.predicates.cloud import VirtualMachinePredicates
from org.jclouds.abiquo.predicates.infrastructure import MachinePredicates


class VmPlugin:
    """ Virtual machine plugin. """
    def __init__(self):
        pass

    def info(self):
        """ Get the information of the plugin. """
        info = {}
        info['name'] = "vm"
        info['description'] = "Virtual machine plugin"
        return info

    def commands(self):
        """ Get the commands provided by the plugin, mapped to the handler methods. """
        commands = {}
        commands['list'] = self.list
        commands['find'] = self.find
        return commands

    def list(self, args):
        """ List all virtual machines. """
        context = ContextLoader().load_context("http://10.60.1.222/api", "admin", "xabiquo")
        try:
            cloud = context.getCloudService()
            vms = cloud.listVirtualMachines()
            print vms
        finally:
            context.close()

    def find(self, args):
        """ Find a virtual machine given its name. """
        # Parse user input to get the name of the virtual machine
        parser = OptionParser(usage="vm find <options>")
        parser.add_option("-n", "--name", help="The name of the virtual machine to find", action="store", dest="name")
        (options, args) = parser.parse_args(args)
        name = options.name
        if not name:
            parser.print_help()
            return

        # Once user input has been read, find the VM
        context = ContextLoader().load_context("http://10.60.1.222/api", "admin", "xabiquo")
        try:
            cloud = context.getCloudService()
            vm = cloud.findVirtualMachine(VirtualMachinePredicates.name(name))
            if vm:
                print "Found virtual machine in: "
                print "  %s" % vm.getVirtualAppliance()
                print "  %s" % vm.getVirtualDatacenter()
                print "  %s" % vm.getEnterprise()
                if vm.getState().existsInHypervisor():
                    admin = self.__context.getAdministrationService()
                    machine = admin.findMachine(MachinePredicates.ip(vm.getVncAddress()))
                    print "  %s" % machine
                else:
                    print "  Machine [None (VM not deployed)]"
            else:
                print "No virtual machine found with name: %s" % name
                vms = cloud.listVirtualMachines()
                print vms
        finally:
            context.close()

def load():
    """ Loads the current plugin. """
    return VmPlugin()

