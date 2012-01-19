import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

def speed(ip, community, type):
    # In: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.10.2
    # Out: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.16.2
    mib_ifout = "1.3.6.1.2.1.2.2.1.16"
    mib_ifin  = "1.3.6.1.2.1.2.2.1.10"
    if type == 'out':
        value = tuple([int(i) for i in mib_ifout.split('.')])
    elif type == 'in':
        value = tuple([int(i) for i in mib_ifin.split('.')])

    generator = cmdgen.CommandGenerator()
    comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))

    real_fun = getattr(generator, 'nextCmd')

    res = (errorIndication, errorStatus, errorIndex, varBindTable)\
            = real_fun(comm_data, transport, value)

    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
    else:
        for varBindTableRow in varBindTable:
            # varBindTableRow:
            #   [(ObjectName(1.3.6.1.2.1.2.2.1.10.8), Counter32(180283794))]
            data = varBindTableRow[0]
            port = data[0]._value[len(value):]
            speed = data[1]

            yield {'port': port[0], 'speed': speed, 'type': type}

if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        community = sys.argv[2]
        type = sys.argv[3]
    except IndexError:
        print "Please run command like:"
        print "python traffic.py <ip> <community> <'in'/'out'>"
        sys.exit(0)

    for traffic in speed(ip, community, type):
        print 'port: %(port)s speed: %(speed)s type: %(type)s' % traffic

