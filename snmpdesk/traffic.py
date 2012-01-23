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
            # varBindTableRow:
            #   in: [(ObjectName(1.3.6.1.2.1.2.2.1.10.8), Counter32(180283794))]
            data = varBindTableRow[0]
            port = data[0]._value[len(value):]
            octets = data[1]

            yield {'port': port[0], 'octets': octets}

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
        data = datafrommib(mib[0], community, ip)
        for row in data:
            if row:
                ports[row['port']][mib[1]] = int(row['octets'])
            else:
                return None

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
    if ports:
        for key, value in ports.items():
            print key, ('in: %(in)s out: %(out)s ucast: %(ucast)s' +\
                       ' nucast: %(nucast)s discards: %(discards)s' +\
                       ' errors: %(errors)s') % value

