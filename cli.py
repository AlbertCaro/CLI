import os

import time


def host():
    file = open('hostname.txt','r')
    hostname = file.readline()
    file.close()
    if len(hostname) < 1:
        hostname = "Switch"
    return hostname

def Interface():
    hostname = host()
    flag = True
    while flag:
        comm = input(hostname+"(config-if)# ")
        if comm == "":
            print()
        elif comm == "exit":
            flag = False
        else:
            print("Comando no reconocido.")

def passExec(passw):
    file = open('password.txt','w')
    file.write(passw+" 0")
    file.close()


def login():
    file = open('password.txt','r')
    passw = file.readline()
    file.close()
    file = open('password.txt', 'w')
    file.write(passw[0:len(passw) - 2]+" 1")
    file.close()

def Line():
    hostname = host()
    flag = True
    while flag:
        comm = input(hostname+"(config-line)# ")
        comm = comm.split(" ")
        if comm[0] == "password":
            passExec(comm[1])
        elif comm[0] == "login":
            login()
        elif comm[0] == "exit":
            flag = False
        else:
            print("Comando no reconocido.")

def confPassword(passw):
    file = open('exec.txt','w')
    file.write(passw)
    file.close()

def confSecret(secret):
    file = open('exec.txt', 'w')
    file.write(secret)
    file.close()

def changeHostname(name):
    file = open('hostname.txt', 'w')
    file.write(name)
    file.close()

def banner_motd(comm):
    pos1 = comm.find("#")+1
    pos2 = len(comm)-1
    banner = comm[pos1:pos2]
    file = open('banner_motd.txt','w')
    file.write(banner)
    file.close()

def Conf():
    flag = True
    while flag:
        hostname = host()
        comm = input(hostname+"(config)# ")
        comm = comm.split(" ")
        if comm[0] == "line":
            if len(comm) > 1 and len(comm) < 5:
                Line()
            elif len(comm) > 4:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "interface":
            if len(comm) > 1 and len(comm) < 3:
                Interface()
            elif len(comm) > 2:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "enable":
            if len(comm) > 2 and len(comm) < 4:
                if comm[1] == "password":
                    confPassword(comm[2])
                elif comm[1] == "secret":
                    confSecret(comm[2])
            elif len(comm) > 3:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "hostname":
            if len(comm) > 1 and len(comm) < 3:
                changeHostname(comm[1])
            elif len(comm) > 2:
                input("Invalid input detected")
            else:
                input("% Incomplete command")
        elif comm[0] == "banner":
            if len(comm) > 1:
                comm = " ".join(comm)
                banner_motd(comm)
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

def Exec():
    file = open('exec.txt', 'r')
    password = file.readline()
    file.close()
    passw = str("null")
    if len(password) > 0:
        while passw != password:
            passw = input("Password: ")
    flag = True
    while flag:
        hostname = host()
        comm = input(hostname+"# ")
        if comm == "conf term" or comm == "config terminal" or comm == "config term" or comm == "configure terminal":
            Conf()
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

def ping(ip):
    print('''\nType escape sequence to abort.
Sending 5, 100-byte ICMP Echos to '''+ip+''', timeout is 2 seconds:''')
    for x in range(0,5):
        print(".")
        time.sleep(2)
    print("\nSuccess rate is 5 percent (5/5)\n")

def start():
    file = open('banner_motd.txt','r')
    banner = file.readline()
    file.close()

    file = open('password.txt', 'r')
    text = file.readline()
    file.close()

    passw = str("null")
    if len(banner) > 0:
        print(banner+"\n")

    if text != "":
        text = text.split(" ")
        password = text[0]
        login = text[1]
        if login == '1':
            rep = True
            print("User Access Verification\n")
            while passw!=password:
                passw = input("Password: ")
            print()
    flag = True

    while flag:
        hostname = host()
        comm = input(hostname+"> ")
        comm = comm.split(" ")
        if comm[0] == "enable":
            Exec()
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
    clear = lambda: os.system('cls')
    clear()
    starting = input("")
    clear()
    if starting == "exit":
        flag = False
    else:
        start()