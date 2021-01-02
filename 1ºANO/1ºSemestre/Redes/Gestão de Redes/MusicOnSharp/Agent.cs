using System;
using System.Net;
using Lextm.SharpSnmpLib;
using Lextm.SharpSnmpLib.Messaging;
using Lextm.SharpSnmpLib.Security;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{

    public class Agent
    {
        private readonly SnmpEngine engine;
        public  Agent()
        {
           

            var store = new ObjectStore();

            store.Add(new musicListTable());
            var users = new UserRegistry();
            users.Add(new OctetString("neither"), DefaultPrivacyProvider.DefaultPair);
            users.Add(new OctetString("authen"), new DefaultPrivacyProvider(new MD5AuthenticationProvider(new OctetString("authentication"))));
            if (DESPrivacyProvider.IsSupported)
            {
                users.Add(new OctetString("privacy"), new DESPrivacyProvider(new OctetString("privacyphrase"), new MD5AuthenticationProvider(new OctetString("authentication"))));
            }

            if (AESPrivacyProviderBase.IsSupported)
            {
                users.Add(new OctetString("aes"), new AESPrivacyProvider(new OctetString("privacyphrase"), new MD5AuthenticationProvider(new OctetString("authentication"))));
                users.Add(new OctetString("aes192"), new AES192PrivacyProvider(new OctetString("privacyphrase"), new MD5AuthenticationProvider(new OctetString("authentication"))));
                users.Add(new OctetString("aes256"), new AES256PrivacyProvider(new OctetString("privacyphrase"), new MD5AuthenticationProvider(new OctetString("authentication"))));
            }

            var getv1 = new GetV1MessageHandler();
            var getv1Mapping = new HandlerMapping("v1", "GET", getv1);

            var getv23 = new GetMessageHandler();
            var getv23Mapping = new HandlerMapping("v2,v3", "GET", getv23);

            var setv1 = new SetV1MessageHandler();
            var setv1Mapping = new HandlerMapping("v1", "SET", setv1);

            var setv23 = new SetMessageHandler();
            var setv23Mapping = new HandlerMapping("v2,v3", "SET", setv23);

            var getnextv1 = new GetNextV1MessageHandler();
            var getnextv1Mapping = new HandlerMapping("v1", "GETNEXT", getnextv1);

            var getnextv23 = new GetNextMessageHandler();
            var getnextv23Mapping = new HandlerMapping("v2,v3", "GETNEXT", getnextv23);

            var getbulk = new GetBulkMessageHandler();
            var getbulkMapping = new HandlerMapping("v2,v3", "GETBULK", getbulk);

            var v1 = new Version1MembershipProvider(new OctetString("public"), new OctetString("public"));
            var v2 = new Version2MembershipProvider(new OctetString("public"), new OctetString("public"));
            var v3 = new Version3MembershipProvider();
            var membership = new ComposedMembershipProvider(new IMembershipProvider[] { v1, v2, v3 });
            var handlerFactory = new MessageHandlerFactory(new[]
            {
                getv1Mapping,
                getv23Mapping,
                setv1Mapping,
                setv23Mapping,
                getnextv1Mapping,
                getnextv23Mapping,
                getbulkMapping
            });

            var pipelineFactory = new SnmpApplicationFactory(store, membership, handlerFactory);
             engine = new SnmpEngine(pipelineFactory, new Listener { Users = users }, new EngineGroup());
            engine.ExceptionRaised += Engine_ExceptionRaised;
            engine.Listener.MessageReceived += RequestReceived;
                engine.Listener.AddBinding(new IPEndPoint(IPAddress.Any, 2003));
                
                //getmusicInfo.info();

            }
            public  void Start() {
                engine.Start();
            }
            public  void Dispose() {
                engine.Dispose();
            }
        

          private static void Engine_ExceptionRaised(object sender, ExceptionRaisedEventArgs e)
        {
            Console.WriteLine("Exception occurred: {0}", e.Exception);
        }

        private static void RequestReceived(object sender, MessageReceivedEventArgs e)
        {
            Console.WriteLine("Message version {0}: {1}", e.Message.Version, e.Message);
        }
    }

}
       
