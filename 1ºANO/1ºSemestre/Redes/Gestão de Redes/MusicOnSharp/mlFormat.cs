using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
    internal sealed class mlFormat : ScalarObject
    {
        private readonly OctetString _data;
        public mlFormat (int index, OctetString format) : base("1.3.6.1.3.4.1.5.{0}", index)
        {
            _data = format;
        }

        public override ISnmpData Data
        {
            get { return _data; }
            set { throw new AccessFailureException(); }
        }


    }
}