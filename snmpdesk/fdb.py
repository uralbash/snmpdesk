import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

def fetchFdb(ip, community):
    mib = '1.3.6.1.2.1.17.7.1.2.2.1.2'
    value = tuple([int(i) for i in mib.split('.')])
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
            #     [(ObjectName(1.3.6.1.2.1.17.7.1.2.2.1.2.5.0.27.144.212.92.45),
            #     Integer(27))]

            data = varBindTableRow[0][0]._value[len(value):]

            vlan = data[0]
            #mac = '%s' % ':'.join([hex(int(i))[2:] for i in data[-6:]])
            mac = '%02x:%02x:%02x:%02x:%02x:%02x' % tuple(map(int, data[-6:]))
            port = varBindTableRow[0][1]
            yield {'vlan': vlan, 'mac': mac, 'port': port}

if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        community = sys.argv[2]
    except IndexError:
        print "PLease run command like:"
        print "python %s <ip> <community>" % __file__
        sys.exit(0)

    for fdb in fetchFdb(ip, community):
        print 'vlan: %(vlan)s mac: %(mac)s port: %(port)s' % (fdb)

