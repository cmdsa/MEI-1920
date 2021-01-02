using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Lextm.SharpSnmpLib;
using MusicOnSharp.Pipeline;

namespace MusicOnSharp
{
   
    public sealed class musicListTable : TableObject
    {
        // "1.3.6.1.2.1.1.9.1"
        private readonly IList<ScalarObject> _elements = new List<ScalarObject>();

   
        int a= 1,b= 1,c= 1,d = 1,e = 1;
        public musicListTable()
        {
            var files = Directory.EnumerateFiles("wwwroot/music/", "*.*", SearchOption.AllDirectories)
            .Where(s => s.EndsWith(".mp3") || s.EndsWith(".wav") || s.EndsWith(".flac") );
            
            foreach(var stuff in files)
            {   
                _elements.Add(new mlIndex(a));
                a++;
            }
            
            foreach(var stuff in files)
            {   
                
                var tfile = TagLib.File.Create(stuff);
                string title = tfile.Tag.Title;
                var name = Path.GetFileName(stuff);
                _elements.Add(new mlTitle(b,  new OctetString(name.ToString())));
                b++;
            }

             foreach(var stuff in files)
            {   
               
                var tfile = TagLib.File.Create(stuff);
                string artist = tfile.Tag.FirstAlbumArtist;
                if (artist == null)
                {
                    artist = "none";
                }
 
                _elements.Add(new mlArtist(c, new OctetString(artist.ToString())));
                c++;
            }

             foreach(var stuff in files)
            {   
                var tfile = TagLib.File.Create(stuff);

                string genre = tfile.Tag.FirstGenre;

                _elements.Add(new mlGenre(d,  new OctetString(genre.ToString())));
                d++;
            }

             foreach(var stuff in files)
            {   

                string extension = Path.GetExtension(stuff);

                _elements.Add(new mlFormat(e,  new OctetString(extension.ToString())));
                 e++;
            }

             /*foreach(var stuff in files)
            {   
                i++;
                var tfile = TagLib.File.Create(stuff);
                string title = tfile.Tag.Title;
                string album = tfile.Tag.Album;
                string extension = Path.GetExtension(stuff);
                TimeSpan duration = tfile.Properties.Duration;
                string artist = tfile.Tag.FirstAlbumArtist;
                if (artist == null)
                {
                    artist = "none";
                }
                string genre = tfile.Tag.FirstGenre;
                 Console.WriteLine("Title: {0},album: {1}, artist: {2}, genre {4}, duration: {3}, extension: {5} ", title,album,artist, duration,genre,extension);
                _elements.Add(new mlIndex(i));
                _elements.Add(new mlTitle(i,  new OctetString(title.ToString())));
                _elements.Add(new mlArtist(i, new OctetString(artist.ToString())));
                _elements.Add(new mlGenre(i,  new OctetString(genre.ToString())));
                _elements.Add(new mlFormat(i,  new OctetString(extension.ToString())));
                 Console.WriteLine(i);
            }*/
            
            
        
            
           
        }

        /// <summary>
        /// Gets the objects in the table.
        /// </summary>
        /// <value>The objects.</value>
        protected override IEnumerable<ScalarObject> Objects
        {
            get { return _elements; }
        }
    }
}