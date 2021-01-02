using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
    internal sealed class mlIndex : ScalarObject
    {
        private readonly ISnmpData _data;
        public mlIndex(int index) : base("1.3.6.1.3.4.1.1.{0}", index)
        {
            _data = new Integer32(index);
        }

        public override ISnmpData Data
        {
            get { return _data; }
            set { throw new AccessFailureException(); }
        }


    }
}