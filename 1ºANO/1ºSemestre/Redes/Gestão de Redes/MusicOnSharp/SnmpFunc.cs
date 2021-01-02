using System.Collections.Generic;
using System.Net;
using Lextm.SharpSnmpLib;
using Lextm.SharpSnmpLib.Messaging;


namespace MusicOnSharp
{
    class SnmpFunc
    {
        public List<Variable> BulkWalk(string oid,string localhost = "127.0.0.1",int PortUDP = 2003)
        {
            var result = new List<Variable>();
            Messenger.BulkWalk(VersionCode.V2,
                new IPEndPoint(IPAddress.Parse(localhost), PortUDP),
                new OctetString("public"),
                new OctetString(""), 
                new ObjectIdentifier(oid),
                result,
                60000,
                10,
                WalkMode.WithinSubtree,
                null,
                null);

            return result;
        }
    }

}