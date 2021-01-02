using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
    internal sealed class mlArtist : ScalarObject
    {
        private readonly OctetString _data;
        public mlArtist (int index, OctetString artist) : base("1.3.6.1.3.4.1.3.{0}", index)
        {
            _data = artist;
        }

        public override ISnmpData Data
        {
            get { return _data; }
            set { throw new AccessFailureException(); }
        }


    }
}