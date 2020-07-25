
module getcert_CMD;
import std.stdio;
import std.digest.sha;
import std.string : representation,strip;
import std.net.curl;
import std.getopt;
import std.base64;
import std.process;
import std.array;
import core.stdc.stdlib:exit;

   // find and substitute all matching authors


    string url = "https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/CCMovelDigitalSignature.svc?wsdl";
    string SOAP_ACTION = "http://Ama.Authentication.Service/CCMovelSignature/GetCertificate";



public string[] getCertificate(string ApplicationId, string UserId)
{
    string encodestring = Base64.encode(ApplicationId.representation);
    //string encodestring = Base64.encode("b826359c-06f8-425e-8ec3-50a97a418916".representation);
    
    //string soapreq = sendSOAPrequest(encodestring, "+351 935423080");
    string soapreq;
    
    soapreq = sendSOAPrequest(encodestring, UserId);

    string[]  certs = parseResponse(soapreq);
    return certs;
}

private string[] parseResponse(string response) {
        //string[] splitedresp = response.split("</GetCertificateResult>");
        //string allcerts = splitedresp[1];
        string[] tempcerts = new string[3];
        tempcerts = response.split("-----BEGIN CERTIFICATE-----");
        
        if (tempcerts.length < 2)
        {
            writeln("Impossível obter certificado");
            exit(0);
        }
        int total = cast(int)tempcerts.length;
       
        int i = 0;
        while(i < total)
        {
            tempcerts[i] = "-----BEGIN CERTIFICATE-----" ~ tempcerts[i];
            i++;
        }
        string[] certificates = new string[3];
        certificates[0] = tempcerts[1].replace("&#xD;", "");
        certificates[1] = tempcerts[3].replace("&#xD;", "");
        certificates[1] = certificates[1].replace("</GetCertificateResult></GetCertificateResponse></s:Body></s:Envelope>","");
        certificates[2] = tempcerts[2].replace("&#xD;", "");
        return certificates;
    }

private string sendSOAPrequest(string applicationId,string userId)
{
     string response = "";
    try {

	        auto body =  "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">" ~
                    "<soapenv:Header/>" ~
                    "<soapenv:Body>" ~
                    "<GetCertificate xmlns=\"http://Ama.Authentication.Service/\">" ~
                    "<applicationId>" ~ applicationId ~ "</applicationId>" ~
                    "<userId>" ~ userId ~ "</userId>" ~
                    "</GetCertificate>" ~
                    "</soapenv:Body>" ~
                    "</soapenv:Envelope>";

	
	
        	auto http = HTTP(url);
	        http.addRequestHeader("SOAPAction", SOAP_ACTION);
            http.addRequestHeader("Content-type", "text/xml");
	        http.setPostData(body, "text/xml");
   
	        http.onReceive = (ubyte[] data) {response = cast(string)data; return data.length; };
	        http.perform();

        }
        catch (Exception e)
        {
            response = "Error";
        }

	return response;

}

    

