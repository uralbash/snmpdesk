import sys
import collections
from pysnmp.entity.rfc3413.oneliner import cmdgen

def datafrommib(mib, community, ip):
    value = tuple([int(i) for i in mib.split('.')])
    generator = cmdgen.CommandGenerator()
    comm_data = cmdgen.CommunityData('server', community, 1) # 1 means version SNMP v2c
    transport = cmdgen.UdpTransportTarget((ip, 161))

    real_fun = getattr(generator, 'nextCmd')
    res = (errorIndication, errorStatus, errorIndex, varBindTable)\
            = real_fun(comm_data, transport, value)

    if not errorIndication is None  or errorStatus is True:
           print "Error: %s %s %s %s" % res
           yield None
    else:
        for varBindTableRow in varBindTable:
            data = varBindTableRow[0]
            port = data[0]._value[len(value):]
            octets = data[1]

            yield {'port': port[0], 'octets': octets}

def status(ip, community):
    # for use snmptool try:
    # snmpwalk -c mymypub -v2c <ip> <mib>
    # e.t.c...
    mibs = [('1.3.6.1.2.1.2.2.1.8', 'ifOperStatus'),
            ('1.3.6.1.2.1.2.2.1.3', 'ifType'),
            ('1.3.6.1.2.1.2.2.1.5', 'ifSpeed'),
            ('1.3.6.1.2.1.31.1.1.1.1', 'ifName'),
            ('1.3.6.1.2.1.31.1.1.1.18', 'ifAlias')
            ]

    ports = collections.defaultdict(dict)

    for mib in mibs:
        data = datafrommib(mib[0], community, ip)
        for row in data:
            if row:
                ports[row['port']][mib[1]] = row['octets']
            else:
                return None

    return ports

if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        community = sys.argv[2]
    except IndexError:
        print "Please run command like:"
        print "python %s <ip> <community>" % (__file__)
        sys.exit(0)

    ports = status(ip, community)
    if ports:
        for key, value in ports.items():
            print key, ('ifOperStatus: %(ifOperStatus)s ifType: %(ifType)s' +\
                        ' ifSpeed: %(ifSpeed)s ifName: %(ifName)s' +\
                        ' ifAlias: %(ifAlias)s') % value

