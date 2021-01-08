
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Blazorise.Charts;
using Blazorise.Charts.Streaming;
using Lextm.SharpSnmpLib;
using Microsoft.AspNetCore.Components;
using SNMPSERVER.Data;


namespace SNMPSERVER.Pages
{

    public partial class Testpage : ComponentBase
    {

        //SNMP STUFF
         IpPortFormData ipPortForm = new IpPortFormData();
        private static SnmpFunc snmpFunc = new SnmpFunc();
        public  List<Variable> processname; 
        public  List<Variable> processmemory;
        public  List<Variable> processusage;
        public  List<Variable> indexprocess;
        
        public string ipAdress;
        public int PortNumber;
        public System.Threading.Timer timer;
        public int howmany=0;
        public int memoryValue,cpuValue;
        
        public int iGlobal;

        //Charts Stuff
         public LineChart<LiveDataPoint> memoryLineChart;
         public LineChart<LiveDataPoint> cpuLineChart;
         public LineChart<LiveDataPoint> totalChart;
      

        public void  start()
        {
            ipAdress = ipPortForm.IpAdress;
            PortNumber = ipPortForm.portNumb;
           
            Console.WriteLine("{0}  {1}",PortNumber,ipAdress);
            processname = snmpFunc.BulkWalk("1.3.6.1.2.1.25.4.2.1.2",ipAdress,PortNumber);
            processmemory = snmpFunc.BulkWalk("1.3.6.1.2.1.25.5.1.1.2",ipAdress,PortNumber);
            processusage = snmpFunc.BulkWalk("1.3.6.1.2.1.25.5.1.1.1",ipAdress,PortNumber);
            indexprocess = snmpFunc.BulkWalk("1.3.6.1.2.1.25.4.2.1.1",ipAdress,PortNumber);
            
            timer = new System.Threading.Timer(async _ =>
            {
                await ValuesChanged();
            },  
                null, 
                TimeSpan.Zero, 
                TimeSpan.FromSeconds(5));

        }

        public Task ValuesChanged()
        {
            //Console.WriteLine("abcde");
            processname = snmpFunc.BulkWalk("1.3.6.1.2.1.25.4.2.1.2",ipAdress,PortNumber);
            processmemory = snmpFunc.BulkWalk("1.3.6.1.2.1.25.5.1.1.2",ipAdress,PortNumber);
            processusage = snmpFunc.BulkWalk("1.3.6.1.2.1.25.5.1.1.1",ipAdress,PortNumber);
            indexprocess = snmpFunc.BulkWalk("1.3.6.1.2.1.25.4.2.1.1",ipAdress,PortNumber);
            if(iGlobal > indexprocess.Count())
            {
                iGlobal--;
                memoryLineChart.Clear();
                cpuLineChart.Clear();
            }
            memoryValue = Int32.Parse(processmemory[iGlobal].Data.ToString());
            cpuValue = Int32.Parse(processusage[iGlobal].Data.ToString());
            Console.WriteLine(memoryValue);
            InvokeAsync(StateHasChanged);
            return Task.CompletedTask;
        }

    
        

       

        string[] Labels = { "Red", "Blue", "Yellow", "Green", "Purple", "Orange" };
        List<string> backgroundColors = new List<string> { ChartColor.FromRgba( 255, 99, 132, 0.5f ), ChartColor.FromRgba( 54, 162, 235, 0.5f ), ChartColor.FromRgba( 255, 206, 86, 0.5f ), ChartColor.FromRgba( 75, 192, 192, 0.5f ), ChartColor.FromRgba( 153, 102, 255, 0.5f ), ChartColor.FromRgba( 255, 159, 64, 0.5f ) };
        List<string> borderColors = new List<string> { ChartColor.FromRgba( 255, 99, 132, 1f ), ChartColor.FromRgba( 54, 162, 235, 1f ), ChartColor.FromRgba( 255, 206, 86, 1f ), ChartColor.FromRgba( 75, 192, 192, 1f ), ChartColor.FromRgba( 153, 102, 255, 1f ), ChartColor.FromRgba( 255, 159, 64, 1f ) };

        public struct LiveDataPoint
        {
            public object X { get; set; }

            public object Y { get; set; }
        }

        public object memoryLineChartOptions = new
        {
            Title = new
            {
                Display = true,
                Text = "Memory Usage"
            },
            Scales = new
            {
                YAxes = new object[]
                {
                    new {
                        ScaleLabel = new {
                        Display = true, LabelString = "value" }
                    }
                }
            },
            Tooltips = new
            {
                Mode = "nearest",
                Intersect = false
            },
            Hover = new
            {
                Mode = "nearest",
                Intersect = false
            }
        };
        public object cpuLineChartOptions = new
        {
            Title = new
            {
                Display = true,
                Text = "Cpu Usage"
            },
            Scales = new
            {
                YAxes = new object[]
                {
                    new {
                        ScaleLabel = new {
                        Display = true, LabelString = "value" }
                    }
                }
            },
            Tooltips = new
            {
                Mode = "nearest",
                Intersect = false
            },
            Hover = new
            {
                Mode = "nearest",
                Intersect = false
            }
        };
         public object TotalLineChartOptions = new
        {
            Title = new
            {
                Display = true,
                Text = "Processos Totais"
            },
            Scales = new
            {
                YAxes = new object[]
                {
                    new {
                        ScaleLabel = new {
                        Display = true, LabelString = "value" }
                    }
                }
            },
            Tooltips = new
            {
                Mode = "nearest",
                Intersect = false
            },
            Hover = new
            {
                Mode = "nearest",
                Intersect = false
            }
        };
        
   
         public async Task Draw()
        {

                await Task.WhenAll(
                    HandleRedraw( memoryLineChart,  MemoryUsage ),
                    HandleRedraw( cpuLineChart,  CpuUsage )
                  );
        
        }
        public async Task drawStart()
        {

                await Task.WhenAll(
                   
                    HandleRedraw( totalChart,  TotalProcess ));
        
        }

        async Task HandleRedraw<TDataSet, TItem, TOptions, TModel>( BaseChart<TDataSet, TItem, TOptions, TModel> chart, params Func<TDataSet>[] getDataSets )
            where TDataSet : ChartDataset<TItem>
            where TOptions : ChartOptions
            where TModel : ChartModel
        {
            await chart.Clear();

            await chart.AddLabelsDatasetsAndUpdate( Labels, getDataSets.Select( x => x.Invoke() ).ToArray() );
        }

      

     LineChartDataset<LiveDataPoint> MemoryUsage()
        {
            return new LineChartDataset<LiveDataPoint>
            {
                Data = new List<LiveDataPoint>(),
                Label = "Memory Usage (total) " + processname[iGlobal].Data.ToString(),
                BackgroundColor = backgroundColors[1],
                BorderColor = borderColors[1],
                Fill = false,
                CubicInterpolationMode = "default",
            };
        }

        LineChartDataset<LiveDataPoint> CpuUsage()
        {
            return new LineChartDataset<LiveDataPoint>
            {
                Data = new List<LiveDataPoint>(),
                Label = "Cpu Usage (total) " + processname[iGlobal].Data.ToString(),
                BackgroundColor = backgroundColors[2],
                BorderColor = borderColors[2],
                Fill = false,
                CubicInterpolationMode = "default",
            };
        }
        LineChartDataset<LiveDataPoint> TotalProcess()
        {
            return new LineChartDataset<LiveDataPoint>
            {
                Data = new List<LiveDataPoint>(),
                Label = "Nº processos (total):  " + indexprocess.Count(),
                BackgroundColor = backgroundColors[3],
                BorderColor = borderColors[3],
                Fill = false,
                CubicInterpolationMode = "default",
            };
        }

        public Task OnMemoryUsageLineRefreshed( ChartStreamingData<LiveDataPoint> data )
        {
            data.Value = new LiveDataPoint
            {
                X = DateTime.Now,
                Y = memoryValue,
                
            };
            //Console.WriteLine( processmemory[10].Data.ToBytes());
            return Task.CompletedTask;
        }
               public Task OnCPUUsageRefreshed( ChartStreamingData<LiveDataPoint> data )
        {
            data.Value = new LiveDataPoint
            {
                X = DateTime.Now,
                Y = cpuValue,
                
            };
            //Console.WriteLine( processmemory[10].Data.ToBytes());
            return Task.CompletedTask;
        }

                      public Task OnTotalRefresh( ChartStreamingData<LiveDataPoint> data )
        {
            data.Value = new LiveDataPoint
            {
                X = DateTime.Now,
                Y = indexprocess.Count(),
                
            };
            //Console.WriteLine( processmemory[10].Data.ToBytes());
            return Task.CompletedTask;
        }

       

        public async Task Edit(int i)
        {
            //Console.WriteLine($"Edit item: {processmemory[i].Data} and {processusage[i].Data}");
             memoryValue = Int32.Parse(processmemory[i].Data.ToString());
             cpuValue = Int32.Parse(processusage[i].Data.ToString());
             iGlobal = i;
            // var value = indexprocess.FindIndex(s => Variable.Equals(s,val));
            // Console.WriteLine("here is my value: "+ value);
            await Draw();
        }

      
    }
}