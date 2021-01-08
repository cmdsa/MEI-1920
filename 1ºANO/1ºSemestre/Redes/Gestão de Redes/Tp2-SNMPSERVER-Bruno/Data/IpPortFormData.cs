using System;
using System.ComponentModel.DataAnnotations;

namespace SNMPSERVER.Data
{
    public class IpPortFormData
    {
        [RegularExpression("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",ErrorMessage = "O endereço de Ip não é valido")]
        public string IpAdress {get;set;}
        
        [Range(1, 65535, ErrorMessage = "Numbero tem de ser entre 1-65535")]
        public int portNumb {get;set;}
    }
}