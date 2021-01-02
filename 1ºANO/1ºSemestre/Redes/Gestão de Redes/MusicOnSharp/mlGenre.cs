using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
    internal sealed class mlGenre : ScalarObject
    {
        private readonly OctetString _data;
        public mlGenre (int index, OctetString genre) : base("1.3.6.1.3.4.1.4.{0}", index)
        {
            _data = genre;
        }

        public override ISnmpData Data
        {
            get { return _data; }
            set { throw new AccessFailureException(); }
        }


    }
}