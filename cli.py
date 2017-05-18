###
# Alberto Caro Navarro
# alberto.cnavarro@alumnos.udg.mx
# 215818158
# Tecnologías de la Información
###

import os
import os.path as path
import getpass
import time

hostnameFile = 'hostname.txt'
execFile = 'exec.txt'
bannerMotdFile = 'banner_motd.txt'
console = 'console 0.txt'


def modify_file(file, value):
    file = open(file, 'w')
    file.write(value)
    file.close()


def open_file(file):
    file = open(file, 'r')
    text = file.read()
    file.close()
    return text


def host():
    if path.exists(hostnameFile):
        hostname = open_file(hostnameFile)
    else:
        hostname = "Switch"
    return hostname


def interf(file):
    flag = True
    while flag:
        comm = input(host() + "(config-if)# ")
        comm = comm.split(" ")
        if comm[0] == "ip":
            if 2 < len(comm) < 5 and comm[1] == "address":
                modify_file(file, comm[2] + " " + comm[3])
            elif 4 < len(comm) < 2:
                print("% Incomplete command.")
            else:
                print("% Invalid input detected.")
        elif " ".join(comm) == "":
            pass
        elif comm[0] == "exit":
            flag = False
        else:
            print("Comando no reconocido.")


def line(file):
    flag = True
    while flag:
        comm = input(host() + "(config-line)# ")
        comm = comm.split(" ")
        if comm[0] == "password":
            modify_file(file, comm[1] + " 0")
        elif comm[0] == "login":
            if path.exists(file):
                passw = open_file(file)
                modify_file(file, passw[0:len(passw)-2] + " 1")
            else:
                print("% Login disabled on line 0, until 'password' is set")
        elif " ".join(comm) == "":
            pass
        elif comm[0] == "exit":
            flag = False
        else:
            print("Comando no reconocido.")


def conf():
    flag = True
    while flag:
        comm = input(host() + "(config)# ")
        comm = comm.split(" ")
        if comm[0] == "line":
            if 1 < len(comm) < 5:
                line(comm[1] + " " + comm[2] + ".txt")
            elif len(comm) > 4:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
        elif comm[0] == "interface":
            do = True
            if comm[1].find("/") > 0:
                pos = comm[1].find("/")
                value = comm[1]
                typeInt = value[:pos]
                num = value[len(value)-1:]
                comm[1] = typeInt + num
                if typeInt == "fa0":
                    if 0 > int(num) > 24:
                        do = False
                elif typeInt == "eth0":
                    if 0 > int(num) > 2:
                        do = False
            if do:
                if 1 < len(comm) < 3:
                    interf(comm[1] + ".txt")
                elif len(comm) > 2:
                    print("Invalid input detected")
                else:
                    print("% Incomplete command")
            else:
                print("%Invalid interface type and number")
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
                modify_file(hostnameFile, comm[1])
            elif len(comm) > 2:
                print("Invalid input detected")
            else:
                print("% Incomplete command")
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
            print("%SYS-5-CONFIG_I: Configured from console by console")
            getpass.getpass('')
            flag = False
        elif " ".join(comm) == "":
            pass
        else:
            print("Comando no reconocido.")


def ping(ip):
    print('''\nType escape sequence to abort.
Sending 5, 100-byte ICMP Echos to ''' + ip + ''', timeout is 2 seconds:''')
    for x in range(0, 5):
        time.sleep(2)
        print(".")
    print("\nSuccess rate is 5 percent (5/5)\n")


def show_interface(file, num, type):
    if path.exists(file):
        infoIp = open_file(file)
        infoIp = infoIp.split(" ")
        ip = infoIp[0]
    else:
        ip = "unassigned"
    blank1 = ""
    rep = 25 - len(type+"0/"+str(num))
    for i in range(1, rep):
        blank1 = blank1 + " "
    rep = 15 - len(ip)
    blank2 = "      "
    for j in range(1, rep):
        blank2 = blank2 + " "
    print(type+"0/" + str(num) + blank1 + ip + blank2 + "YES manual down")
    print("down")


def traceroute(ip):
    print('''Type escape sequence to abort.
Tracing the route to ''' + ip + '''\n''')
    for i in range(1, 31):
        print(str(i), end="")
        for j in range(0, 3):
            if j < 3:
                print(" * ", end="")
            else:
                print(" * ")
            time.sleep(2)


def running_interface(type, ref, num):
    print(type + "0/" + num)
    if path.exists(ref + num + ".txt"):
        ip = open_file(ref + num + ".txt")
        print(" ip address " + ip)
    print("!")


def running_line(file):
    if path.exists(file):
        info = open_file(file)
        info = info.split(" ")
        login = info[1]
        if login == "1":
            print("login")
    print("!")


def exec_privileged():
    flag = True
    while flag:
        comm = input(host() + "# ")
        comm = comm.split(" ")
        if " ".join(comm) == "conf term" or " ".join(comm) == "config terminal":
            print("Enter configuration commands, one per line.  End with CNTL/Z.")
            conf()
        elif comm[0] == "?":
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
        elif comm[0] == "ping":
            if len(comm) == 1:
                print("% Incomplete command")
            elif len(comm) < 2:
                print("Invalid input detected")
            else:
                ping(comm[1])
        elif " ".join(comm) == "show ip interface brief":
            print("Interface               IP-Address          OK? Method Status")
            print("Protocol")
            for i in range(1, 25):
                show_interface("fa0" + str(i) + ".txt", i, "FastEthernet")
            if path.exists("vlan1.txt"):
                infoIp = open_file("vlan1.txt")
                infoIp = infoIp.split(" ")
                ip = infoIp[0]
            else:
                ip = "unassigned"
            rep = 15 - len(ip)
            blank = "      "
            for j in range(1, rep):
                blank = blank + " "
            for i in range(1, 3):
                show_interface("eth"+str(i)+".txt", i, "GigabitEthernet")
            print("Vlan1                   "+ip+blank+"YES manual")
            print("administratively down down")
        elif comm[0] == "traceroute":
            if 1 < len(comm) < 3:
                traceroute(comm[1])
            elif len(comm) < 2:
                print("% Incomplete command.")
            else:
                print("% Invalid input detected.")
        elif comm[0] == "show":
            if comm[1] == "running-config":

                print('''Building configuration...

Current configuration : 1045 bytes
!
version 12.2
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname '''+host()+'''
!
!
!
!
!
spanning-tree mode pvst
!''')
                for i in range(1, 31):
                    running_interface("FastEthernet", "fa0", str(i))
                for i in range(1, 3):
                    running_interface("GigabitEthernet", "eth0", str(i))
                print("interface Vlan1")
                if path.exists("vlan1.txt"):
                    ip = open_file("vlan1.txt")
                    print(" ip address "+ip)
                else:
                    print(" no ip address")
                print(" shutdown")
                for i in range(0, 4):
                    print("!")
                print("line con 0")
                running_line(console)
                print("line vty 0 4")
                running_line("vty04.txt")
                print("line vty 5 15")
                running_line("vty515.txt")
                for i in range(0, 3):
                    print("!")
                print("end")
        elif comm[0] == "exit" or comm == "disable":
            flag = False
        elif " ".join(comm) == "":
            pass
        else:
            print("Comando no reconocido.")


def exec_normal():
    flag = True
    if path.exists(bannerMotdFile):
        banner = open_file(bannerMotdFile)
        print(banner+"\n")

    if path.exists(console):
        text = open_file(console)
        passw = str("null")
        text = text.split(" ")
        password = text[0]
        login = text[1]
        count = 0
        if login == '1':
            print("User Access Verification\n")
            while count < 3:
                passw = getpass.getpass()
                if password != passw:
                    flag = False
                    count = count + 1
                else:
                    count = 3
                    flag = True
            print()

    while flag:
        comm = input(host() + "> ")
        comm = comm.split(" ")
        if comm[0] == "enable":
            if path.exists(execFile):
                password = open_file(execFile)
                passw = str("null")
                count = 0
                while count < 3:
                    passw = getpass.getpass()
                    if password != passw:
                        execEntry = False
                        count = count + 1
                    else:
                        count = 3
                        execEntry = True
            else:
                execEntry = True
            if execEntry:
                exec_privileged()
                flag = False
            else:
                print("% Bad secrets\n")
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
        elif comm[0] == "traceroute":
            if 1 < len(comm) < 3:
                traceroute(comm[1])
            elif len(comm) < 2:
                print("% Incomplete command.")
            else:
                print("% Invalid input detected.")
        elif " ".join(comm) == "":
            pass
        elif comm[0] == "exit" or comm[0] == "logout":
            flag = False
        else:
            print("Comando no reconocido.")


flag = True
while flag:
    clear = lambda: os.system('cls')
    clear()
    starting = getpass.getpass('')
    clear()
    if starting == "":
        exec_normal()
    else:
        flag = False