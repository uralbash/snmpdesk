import sys
import collections
from pysnmp.entity.rfc3413.oneliner import cmdgen

def datafrommib(mib):
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
            #   in: [(ObjectName(1.3.6.1.2.1.2.2.1.10.8), Counter32(180283794))]
            data = varBindTableRow[0]
            port = data[0]._value[len(value):]
            bits = data[1]

            yield {'port': port[0], 'bits': bits}

def load(ip, community):
    # for use snmptool try:
    # In: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.10.2
    # Out: snmpwalk -c mymypub -v2c <ip> 1.3.6.1.2.1.2.2.1.16.2
    # e.t.c...
    mibs = [('1.3.6.1.2.1.2.2.1.16', 'out'),
            ('1.3.6.1.2.1.2.2.1.10', 'in'),
            ('1.3.6.1.2.1.2.2.1.11', 'ucast'),
            ('1.3.6.1.2.1.2.2.1.12', 'nucast'),
            ('1.3.6.1.2.1.2.2.1.13', 'discards'),
            ('1.3.6.1.2.1.2.2.1.14', 'errors')]

    ports = collections.defaultdict(dict)

    for mib in mibs:
        for data in datafrommib(mib[0]):
            ports[data['port']][mib[1]] = int(data['bits'])

    return ports

if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        community = sys.argv[2]
    except IndexError:
        print "Please run command like:"
        print "python traffic.py <ip> <community>"
        sys.exit(0)

    ports = load(ip, community)
    for key, value in ports.items():
    #    print 'port: %(port)s speed: %(speed)s type: %(type)s' % traffic
        print key, ('in: %(in)s out: %(out)s ucast: %(ucast)s' +\
                   ' nucast: %(nucast)s discards: %(discards)s' +\
                   'errors: %(errors)s') % value

