
using System;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace MusicOnSharp
{
    public class Program
    {   
        static System.Threading.Timer timer;
        public static void Main(string[] args)
        {
             Agent agent = new Agent();
                agent.Start();
            
            timer = new System.Threading.Timer(async _ =>
            {
               agent.Dispose();
               agent = new Agent();
               agent.Start();
                
            },  
                null, 
                TimeSpan.Zero, 
                TimeSpan.FromSeconds(5));
                
            CreateHostBuilder(args).Build().Run();
        }
               public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
