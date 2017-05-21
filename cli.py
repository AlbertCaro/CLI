###
# Alberto Caro Navarro
# alberto.cnavarro@alumnos.udg.mx
# 215818158
# Tecnologías de la Información
###

import os
import os.path as path
import shutil
import getpass
import time
import platform

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
            do = False
            if comm[1] == "console":
                if 2 < len(comm) < 4 and comm[2] == "0":
                    file = comm[1] + " " + comm[2] + ".txt"
                    do = True
                elif len(comm) < 3:
                    print("% Incomplete command")
                else:
                    print("Invalid input detected")
            elif comm[1] == "vty":
                if 2 < len(comm) < 5 and len(comm) != 3 and ((comm[2] == "0" and comm[3] == "4") or (comm[2] == "5" and comm[3] == "15")):
                    file = comm[1] + " " + comm[2] + "" + comm[3] + ".txt"
                    do = True
                elif len(comm) < 3:
                    print("% Incomplete command")
                else:
                    print("Invalid input detected")
            else:
                print("Invalid input detected")
                print("% Incomplete command")
            if do:
                line(file)
        elif comm[0] == "interface":
            interface = comm[1]
            pos = interface.find("/")
            num = interface[pos+1:]
            if pos > 0:
                if interface[:pos] == "eth0":
                    limit = 3
                else:
                    limit = 25
                if 0 < int(num) < limit:
                    interf(interface[:pos] + num + ".txt")
                else:
                    print("Invalid input detected")
            elif comm[1] == "vlan1":
                if 0 < len(comm) < 3:
                    interf("vlan1.txt")
            else:
                print("Invalid input detected")
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
    system = platform.system()
    if system == "Windows":
        count = "-n"
    elif system == "Linux":
        count = "-c"
    os.system("ping " + count + " 4 " + ip)


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
    print(type+"0/" + str(num) + blank1 + ip + blank2 + "YES manual down          down")


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


def configuration(folderO, folderD):
    flag = False
    if path.exists(folderO + execFile):
        flag = True
        shutil.copyfile(folderO + execFile, folderD + execFile)
    if path.exists(folderO + bannerMotdFile):
        flag = True
        shutil.copyfile(folderO + bannerMotdFile, folderD + bannerMotdFile)
    if path.exists(folderO + console):
        flag = True
        shutil.copyfile(folderO + console, folderD + console)
    for i in range(1, 25):
        if path.exists(folderO + "fa0" + str(i) + ".txt"):
            flag = True
            shutil.copyfile(folderO + "fa0" + str(i) + ".txt", folderD + "fa0" + str(i) + ".txt")
    for i in range(1, 3):
        if path.exists(folderO + "eth0" + str(i) + ".txt"):
            flag = True
            shutil.copyfile(folderO + "eth0" + str(i) + ".txt", folderD + "eth0" + str(i) + ".txt")
    if path.exists(folderO + "vlan1.txt"):
        flag = True
        shutil.copyfile(folderO + "vlan1.txt", folderD + "vlan1.txt")
    if path.exists(folderO + "vty 04.txt"):
        flag = True
        shutil.copyfile(folderO + "vty 04.txt", folderD + "vty 04.txt")
    if path.exists(folderO + "vty 515.txt"):
        flag = True
        shutil.copyfile(folderO + "vty 515.txt", folderD + "vty 515.txt")
    return flag


def delete_running(folder):
    if path.exists(folder + execFile):
        os.remove(folder + execFile)
    if path.exists(folder + console):
        os.remove(folder + console)
    for i in range(1, 25):
        if path.exists(folder + "fa0" + str(i) + ".txt"):
            os.remove(folder + "fa0" + str(i) + ".txt")
    for i in range(1, 3):
        if path.exists(folder + "eth0" + str(i) + ".txt"):
            os.remove(folder + "eth0" + str(i) + ".txt")
    if path.exists(folder + "vlan1.txt"):
        os.remove(folder + "vlan1.txt")
    if path.exists(folder + "vty 04.txt"):
        os.remove(folder + "vty 04.txt")
    if path.exists(folder + "vty 515.txt"):
        os.remove(folder + "vty 515.txt")


def delete_extra(file):
    if path.exists(file):
        os.remove(file)


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
            print("Interface               IP-Address          OK? Method Status        Protocol")
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
                show_interface("eth" + str(i) + ".txt", i, "GigabitEthernet")
            print("Vlan1                   "+ip+blank+"YES manual               administratively down")
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
            elif comm[1] == "startup-config":
                if not path.exists("/nvram"):
                    print("startup-config is not present")
        elif " ".join(comm) == "copy running-config startup-config":
            if not path.exists("startup"):
                os.mkdir("startup")
            if not configuration("", "startup/"):
                os.removedirs("startup")
        elif " ".join(comm) == "copy startup-config running-config":
            if path.exists("startup"):
                configuration("startup/", "")
            else:
                pass
        elif comm[0] == "reload":
            confirm = input("Proceed with reload? [confirm] ")
            if confirm == "y" or confirm == "Y" or confirm == "":
                print('''C2960 Boot Loader (C2960-HBOOT-M) Version 12.2(25r)FX, RELEASE SOFTWARE (fc4)
Cisco WS-C2960-24TT (RC32300) processor (revision C0) with 21039K bytes of memory.
2960-24TT starting...
Base ethernet MAC Address: 0090.0C3B.D365
Xmodem file system is available.
Initializing Flash...
flashfs[0]: 1 files, 0 directories
flashfs[0]: 0 orphaned files, 0 orphaned directories
flashfs[0]: Total bytes: 64016384
flashfs[0]: Bytes used: 4414921
flashfs[0]: Bytes available: 59601463
flashfs[0]: flashfs fsck took 1 seconds.
...done Initializing Flash.

Boot Sector Filesystem (bs:) installed, fsid: 3
Parameter Block Filesystem (pb:) installed, fsid: 4


Loading "flash:/c2960-lanbase-mz.122-25.FX.bin"...''')
                for i in range(0, 15):
                    print("#")
                    time.sleep(1)
                delete_extra(bannerMotdFile)
                delete_extra(hostnameFile)
                delete_extra("startup/" + hostnameFile)
                delete_running("")
                delete_running("startup/")
                if path.exists("startup"):
                    os.removedirs("startup")
                print("[OK]")
                print('''              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706




Cisco IOS Software, C2960 Software (C2960-LANBASE-M), Version 12.2(25)FX, RELEASE SOFTWARE (fc1)
Copyright (c) 1986-2005 by Cisco Systems, Inc.
Compiled Wed 12-Oct-05 22:05 by pt_team
Image text-base: 0x80008098, data-base: 0x814129C4



Cisco WS-C2960-24TT (RC32300) processor (revision C0) with 21039K bytes of memory.


24 FastEthernet/IEEE 802.3 interface(s)
2 Gigabit Ethernet/IEEE 802.3 interface(s)

63488K bytes of flash-simulated non-volatile configuration memory.
Base ethernet MAC Address       : 0090.0C3B.D365
Motherboard assembly number     : 73-9832-06
Power supply part number        : 341-0097-02
Motherboard serial number       : FOC103248MJ
Power supply serial number      : DCA102133JA
Model revision number           : B0
Motherboard revision number     : C0
Model number                    : WS-C2960-24TT
System serial number            : FOC1033Z1EY
Top Assembly Part Number        : 800-26671-02
Top Assembly Revision Number    : B0
Version ID                      : V02
CLEI Code Number                : COM3K00BRA
Hardware Board Revision Number  : 0x01


Switch   Ports  Model              SW Version              SW Image
------   -----  -----              ----------              ----------
*    1   26     WS-C2960-24TT      12.2                    C2960-LANBASE-M

Cisco IOS Software, C2960 Software (C2960-LANBASE-M), Version 12.2(25)FX, RELEASE SOFTWARE (fc1)
Copyright (c) 1986-2005 by Cisco Systems, Inc.
Compiled Wed 12-Oct-05 22:05 by pt_team

''')
                getpass.getpass("Press RETURN to get started!")
                flag = False
            else:
                pass
        elif comm[0] == "exit" or comm == "disable":
            flag = False
        elif " ".join(comm) == "":
            pass
        else:
            print("% Invalid input detected.")


def exec_normal():
    flag = True
    if path.exists(bannerMotdFile):
        banner = open_file(bannerMotdFile)
        print(banner + "\n")

    if path.exists(console):
        text = open_file(console)
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
            print("% Invalid input detected.")


flag = True
while flag:
    clear = platform.system()
    if clear == "Windows":
        clear = "cls"
    elif clear == "Linux":
        clear = "clear"
    os.system(clear)
    starting = getpass.getpass('')
    os.system(clear)
    if starting == "":
        configuration("startup/", "")
        exec_normal()
        delete_running("")
    else:
        flag = False