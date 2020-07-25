module CCMovelSign;

import std.stdio;
import std.net.curl;
import std.string : representation,strip;
import std.array;
import std.base64;

    string url = "https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/CCMovelDigitalSignature.svc?wsdl";
    string SOAP_ACTION = "http://Ama.Authentication.Service/CCMovelSignature/CCMovelSign";



    public string ccMovelSign(string applicationId,string docName, string docHash, string pin, string userId)
    {
        string encodestring = Base64.encode(applicationId.representation);
        string response = sendSOAPrequest(encodestring,docName, docHash,pin, userId);
        string processID = parseResponse(response);
        return processID;
    }

    private string parseResponse(string response)
    {
        string[] splited = response.split("<a:ProcessId>");
        string[] anothersplit = splited[1].split("</a:ProcessId>");
        return anothersplit[0];
    }

    private string sendSOAPrequest(string applicationId,string docName, string docHash, string pin, string userId) 
    {
        string response = "";
        //TO DO
        try 
        {
            string body = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">" ~
                    "<soapenv:Body>" ~
                    "<CCMovelSign xmlns=\"http://Ama.Authentication.Service/\">" ~
                    "<request xmlns:a=\"http://schemas.datacontract.org/2004/07/Ama.Structures.CCMovelSignature\" xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">" ~
                    "<a:ApplicationId>"~ applicationId ~"</a:ApplicationId>" ~
                    "<a:DocName>"~ docName ~"</a:DocName>" ~
                    "<a:Hash>"~ docHash ~"</a:Hash>" ~
                    "<a:Pin>"~ pin ~"</a:Pin>" ~
                    "<a:UserId>"~ userId ~"</a:UserId>" ~
                    "</request>" ~
                    "</CCMovelSign>" ~
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