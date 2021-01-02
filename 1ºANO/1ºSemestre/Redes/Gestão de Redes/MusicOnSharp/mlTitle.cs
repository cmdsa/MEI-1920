using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
    internal sealed class mlTitle : ScalarObject
    {
        private readonly OctetString _data;
        public mlTitle(int index, OctetString title) : base("1.3.6.1.3.4.1.2.{0}", index)
        {
            _data = title;
        }

        public override ISnmpData Data
        {
            get { return _data; }
            set { throw new AccessFailureException(); }
        }


    }
}