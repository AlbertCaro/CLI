###
# Alberto Caro Navarro
# alberto.cnavarro@alumnos.udg.mx
# 215818158
# Tecnologías de la Información
###
import os
import os.path as path
import time

hostnameFile = 'hostname.txt'
execFile = 'exec.txt'
bannerMotdFile = 'banner_motd.txt'
passwordFile = 'password.txt'


def create_file(file):
    file = open(file, 'w')
    file.close()


def modify_file(file, value):
    if not path.exists(file):
        create_file(file)
    file = open(file, 'w')
    file.write(value)
    file.close()


def open_file(file):
    file = open(file, 'r')
    text = file.readline()
    file.close()
    return text


def host():
    if path.exists(hostnameFile):
        hostname = open_file(hostnameFile)
    else:
        hostname = "Switch"
    return hostname


def interf():
    hostname = host()
    flag = True
    while flag:
        comm = input(hostname + "(config-if)# ")
        if comm == "":
            print()
        elif comm == "exit":
            flag = False
        else:
            print("Comando no reconocido.")


def line():
    hostname = host()
    flag = True
    while flag:
        comm = input(hostname + "(config-line)# ")
        comm = comm.split(" ")
        if comm[0] == "password":
            modify_file(passwordFile,comm[1]+" 0")
        elif comm[0] == "login":
            passw = open_file(passwordFile)
            modify_file(passwordFile,passw[0:len(passw)-2]+" 1")
        elif comm[0] == "exit":
            flag = False
        else:
            print("Comando no reconocido.")


def conf():
    flag = True
    while flag:
        hostname = host()
        comm = input(hostname + "(config)# ")
        comm = comm.split(" ")
        if comm[0] == "line":
            if 1 < len(comm) < 5:
                line()
            elif len(comm) > 4:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "interface":
            if 1 < len(comm) < 3:
                interf()
            elif len(comm) > 2:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "enable":
            if 2 < len(comm) < 4:
                if comm[1] == "password":
                    modify_file(execFile, comm[2])
                elif comm[1] == "secret":
                    modify_file(execFile, comm[2])
            elif len(comm) > 3:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "hostname":
            if 1 < len(comm) < 3:
                modify_file(hostnameFile,comm[1])
            elif len(comm) > 2:
                input("Invalid input detected")
            else:
                input("% Incomplete command")
        elif comm[0] == "banner":
            if len(comm) > 1:
                comm = " ".join(comm)
                pos1 = comm.find("#") + 1
                pos2 = len(comm) - 1
                banner = comm[pos1:pos2]
                modify_file(bannerMotdFile, banner)
            else:
                print("% Incomplete command")
        elif comm[0] == "?":
            if len(comm) == 1:
                print('''Configure commands:
  access-list        Add an access list entry
  banner             Define a login banner
  boot               Boot Commands
  cdp                Global CDP configuration subcommands
  clock              Configure time-of-day clock
  crypto             Encryption module
  do                 To run exec commands in config mode
  enable             Modify enable password parameters
  end                Exit from configure mode
  exit               Exit from configure mode
  hostname           Set system's network name
  interface          Select an interface to configure
  ip                 Global IP configuration subcommands
  line               Configure a terminal line
  lldp               Global LLDP configuration subcommands
  logging            Modify message logging facilities
  mac                MAC configuration
  mac-address-table  Configure the MAC address table
  mls                mls global commands
  monitor            
  no                 Negate a command or set its defaults
  port-channel       EtherChannel configuration
  privilege          Command privilege parameters
  sdm                Switch database management
  service            Modify use of network based services
  snmp-server        Modify SNMP engine parameters
  spanning-tree      Spanning Tree Subsystem
  username           Establish User Name Authentication
  vlan               Vlan commands
  vtp                Configure global VTP state''')
            else:
                input("Invalid input detected")
        elif comm[0] == "exit" or comm[0] == "end":
            flag = False
        else:
            print("Comando no reconocido.")


def ping(ip):
    print('''\nType escape sequence to abort.
Sending 5, 100-byte ICMP Echos to ''' + ip + ''', timeout is 2 seconds:''')
    for x in range(0, 5):
        print(".")
        time.sleep(2)
    print("\nSuccess rate is 5 percent (5/5)\n")


def exec_privileged():
    if path.exists(execFile):
        password = open_file(execFile)
        passw = str("null")
        while passw != password:
            passw = input("Password: ")
    flag = True
    while flag:
        hostname = host()
        comm = input(hostname + "# ")
        if comm == "conf term" or comm == "config terminal" or comm == "config term" or comm == "configure terminal":
            conf()
        elif comm == "?":
            if len(comm) == 1:
                print('''Exec commands:
  clear       Reset functions
  clock       Manage the system clock
  configure   Enter configuration mode
  connect     Open a terminal connection
  copy        Copy from one file to another
  debug       Debugging functions (see also 'undebug')
  delete      Delete a file
  dir         List files on a filesystem
  disable     Turn off privileged commands
  disconnect  Disconnect an existing network connection
  enable      Turn on privileged commands
  erase       Erase a filesystem
  exit        Exit from the EXEC
  logout      Exit from the EXEC
  more        Display the contents of a file
  no          Disable debugging informations
  ping        Send echo messages
  reload      Halt and perform a cold restart
  resume      Resume an active network connection
  setup       Run the SETUP command facility
  show        Show running system information
  ssh         Open a secure shell client connection
  telnet      Open a telnet connection
  terminal    Set terminal line parameters
  traceroute  Trace route to destination
  undebug     Disable debugging functions (see also 'debug')
  vlan        Configure VLAN parameters
  write       Write running configuration to memory, network, or''')
            else:
                input("Invalid input detected")
        elif comm == "exit" or comm == "disable":
            flag = False
        else:
            print("Comando no reconocido.")


def exec_normal():
    if path.exists(bannerMotdFile):
        banner = open_file(bannerMotdFile)
        print(banner+"\n")
    if path.exists(passwordFile):
        text = open_file(passwordFile)
        passw = str("null")
        text = text.split(" ")
        password = text[0]
        login = text[1]
        if login == '1':
            print("User Access Verification\n")
            while passw != password:
                passw = input("Password: ")
            print()
    flag = True

    while flag:
        hostname = host()
        comm = input(hostname + "> ")
        comm = comm.split(" ")
        if comm[0] == "enable":
            exec_privileged()
        elif comm[0] == "?":
            if len(comm) == 1:
                print('''Exec commands:
      connect     Open a terminal connection
      disable     Turn off privileged commands
      disconnect  Disconnect an existing network connection
      enable      Turn on privileged commands
      exit        Exit from the EXEC
      logout      Exit from the EXEC
      ping        Send echo messages
      resume      Resume an active network connection
      show        Show running system information
      telnet      Open a telnet connection
      terminal    Set terminal line parameters
      traceroute  Trace route to destination''')
            else:
                print("Invalid input detected")
        elif comm[0] == "ping":
            if len(comm) == 1:
                print("% Incomplete command")
            elif len(comm) < 2:
                print("Invalid input detected")
            else:
                ping(comm[1])
        elif comm[0] == "exit" or comm[0] == "logout":
            flag = False
        else:
            print("Comando no reconocido.")


flag = True
while flag:
    clear = lambda: os.system('clear')
    clear()
    starting = input("")
    clear()
    if starting == "exit":
        flag = False
    else:
        exec_normal()
