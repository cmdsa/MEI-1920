module ValidateOTP;
import std.stdio;
import std.net.curl;
import std.string : representation,strip;
import std.array;
import std.base64;

    string url = "https://cmd.autenticacao.gov.pt/Ama.Authentication.Frontend/CCMovelDigitalSignature.svc?wsdl";
    string SOAP_ACTION = "http://Ama.Authentication.Service/CCMovelSignature/ValidateOtp";

    public string[] ValidateOtp(string otp,string processId, string applicationId){
        string encodestring = Base64.encode(applicationId.representation);
        
        string response = sendSoapRequest(otp,processId,encodestring);
        string[] results = parseResponse(response);
        return  results;
    }

    private string[] parseResponse(string response) {
        string[] sigparse = response.split("</a:Signature>");
        string[] sigparse2 = sigparse[0].split("<a:Signature>");
        string[] codeparse = response.split("</a:Code>");
        string[] codeparse2 = codeparse[0].split("<a:Code>");
        string[] msgparse = response.split("</a:Message>");
        string[] msgparse2 = msgparse[0].split("<a:Message>");

        //string signature = parsed[1];
        string[] results = [sigparse2[1],codeparse2[1],msgparse2[1]];
        return  results;
    }

    private string sendSoapRequest(string otp,string processId, string applicationId) {
        string response = "";
        //TO DO
        try 
        {
            string body = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ama=\"http://Ama.Authentication.Service/\">" ~
                    "<soapenv:Body>" ~
                    "<ama:ValidateOtp>" ~
                    "<ama:code>"~ otp ~"</ama:code>" ~
                    "<ama:processId>"~ processId ~"</ama:processId>" ~
                    "<ama:applicationId>"~ applicationId ~"</ama:applicationId>" ~
                    "</ama:ValidateOtp>" ~
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
