import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

def load(ip, community, type):
    # for use snmptool try:
    # In: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.10.2
    # Out: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.16.2
    # e.t.c...
    mib_ifout = '1.3.6.1.2.1.2.2.1.16'
    mib_ifin  = '1.3.6.1.2.1.2.2.1.10'
    mib_ucast = '1.3.6.1.2.1.2.2.1.11'
    mib_nucast = '1.3.6.1.2.1.2.2.1.12'
    mib_discards = '1.3.6.1.2.1.2.2.1.13'
    mib_errors = '1.3.6.1.2.1.2.2.1.14'

    if type == 'out':
        value = tuple([int(i) for i in mib_ifout.split('.')])
    elif type == 'in':
        value = tuple([int(i) for i in mib_ifin.split('.')])
    elif type == 'ucast':
        value = tuple([int(i) for i in mib_ucast.split('.')])
    elif type == 'nucast':
        value = tuple([int(i) for i in mib_nucast.split('.')])
    elif type == 'discards':
        value = tuple([int(i) for i in mib_discards.split('.')])
    elif type == 'errors':
        value = tuple([int(i) for i in mib_errors.split('.')])

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
            #   in: [(ObjectName(1.3.6.1.2.1.2.2.1.10.8), Counter32(180283794))]
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
        print "python traffic.py <ip> <community>" +\
              " <'in'/'out'/'ucast'/'nucast'/'discards'/'errors'>"
        sys.exit(0)

    for traffic in load(ip, community, type):
        print 'port: %(port)s speed: %(speed)s type: %(type)s' % traffic

