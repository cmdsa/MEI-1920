#!/usr/bin/env rdmd
import getcert_CMD;
import CCMovelSign;
import ValidateOTP;
import std.stdio;
import std.getopt;
import deimos.openssl.x509;
import deimos.openssl.x509v3;
import deimos.openssl.pem;
import deimos.openssl.asn1;
import deimos.openssl.evp;
import deimos.openssl.rsa;
import std.string : representation,strip,toStringz;
import std.utf;
import std.array;
import core.stdc.stdlib:exit;
import std.file;
import std.digest.sha;
import std.base64;
import std.regex;
 


const BufSize = 1024;

extern (C)
{
    X509* PEM_read_bio_X509(BIO* bp, X509** x, pem_password_cb* callback, void* u);
	EVP_MD_CTX *EVP_MD_CTX_new();
}
//ADIÇAO DO CODIGO APRESENTADO NO RELATORIO
//Mensagem Erro sempre que parametros Errados 
string msgError(){
   string error = ("Parametros errados!");
   return error;
}
//Verificacao do user ID com regex
string getUserId(string user_ID){
   pattern = "^(\+?351)?9\d\d{7}$";
   if(user_ID.length == 13){
      if(pattern.match(user_ID)){
         writeln("UserID Valido!");
         string UserID = user_ID;
         return UserID;
      }
   }
   else{return msgError();}
}
//Verificacao do PIN apenas pelo numero de caracteres
string getPin(string str_Pin){
   if(str_Pin.length == 4){
      writeln("Pin Valido!");
      string PIN = str_Pin;
      return PIN;
   }
   else{return msgError();}
}
//FALTAVA CHAMAR ESTAS FUNÇOES - Diferença de Versoes do Trabalho

//unica a ser hardcoded é esta
string AppId = "b826359c-06f8-425e-8ec3-50a97a418916";

void main(string[] args)
{  
	if(args[1] == "-h")
		{
			writeln("As opções de cada operação podem ser visualizadas através da \n execução de ./engsegd <oper> -h, em que <oper> é uma das seguintes operações:

    'GetCertificate' ou 'gc'
        testa o comando SOAP GetCertificate do SCMD
    'CCMovelSign' ou 'ms'
        testa o comando SOAP CCMovelSign do SCMD
    'CCMovelMultipleSign' ou 'mms'
        testa o comando SOAP CCMovelMultipleSign do SCMD
    'ValidateOtp' ou 'otp'
        testa o comando SOAP ValidateOtp do SCMD
    'TestAll' ou 'test'
        testa automaticamente a sequência de comandos GetCertificate, CCMovelSign e ValidateOtp, \n verificando no final a assinatura, baseado na assinatura recebida, na hash gerada e na chave pública do certificado recebido.
");
		}
	if(args.length > 2)
	{
		
		}
		if(args[1] == "GetCertificate" || args[1] == "gc")
		{
			if(args[2] == "-h")
			{
				writeln("testa o comando SOAP GetCertificate do SCMD");
				writeln("Exemplo de utilização:");
				writeln("./engsegd gc '+351 999999999'");


			}
			else 
			{
				TestGetCertificate(args[2]);
			}
			
		}
		if(args[1] == "CCMovelSign" || args[1] == "ms")
			{
				if(args[2] == "-h")
				{
					writeln("testa o comando SOAP CCMovelSign do SCMD");
					writeln("Exemplo de utilização:");
					writeln("./engsegd ms '+351 999999999' notas.txt 1111");


				}
				else if(args.length == 5)
				{
					TestccMovil(args[2], args[3],args[4]);
				}
			
			}
			if(args[1] == "TestOTP" || args[1] == "otp")
			{
				if(args[2] == "-h")
				{
					writeln("testa o comando SOAP ValidateOtp do SCMD");
					writeln("Exemplo de utilização:");
					writeln("./engsegd otp '+351 999999999' notas.txt 1111");


				}
				else if(args.length == 5)
				{
					TestOTP(args[2], args[3],args[4]);
				}
			
			}
			if(args[1] == "TestAll" || args[1] == "test")
			{
				if(args[2] == "-h")
				{
					writeln("testa automaticamente a sequência de comandos GetCertificate, CCMovelSign e ValidateOtp,");
					writeln("verificando no final a assinatura, baseado na assinatura recebida, na hash gerada e na chave pública do certificado recebido.");
					writeln("Exemplo de utilização:");
					writeln("./engsegd test '+351 999999999' notas.txt 1111");


				}
				else if(args.length == 5)
				{
					TestAll(args[2], args[3],args[4]);
				}
			
			}
	

	

}	
///testa o comando SOAP GetCertificate do SCMD
void TestGetCertificate(string UserId)
{
	string[] certs = getCertificate(AppId,UserId);
	foreach (string key; certs)
	{
		writeln(key);
	}
}
///testa o comando SOAP CCMovelSign do SCMD
void TestccMovil(string UserId, string filename,string PIN)
{
	string text = readText(filename);
	ubyte[32] sha = sha256Of(text);
	char[] encodedhash =  Base64.encode(sha);
	string ccMovel = ccMovelSign(AppId,filename,cast(string)encodedhash,PIN,UserId);
	writeln("ProcessID devolvido pela operação CCMovelSign: " ~ ccMovel);
}
///testa o comando SOAP ValidateOtp do SCMD
void TestOTP(string UserId, string filename,string PIN)
{
	string text = readText(filename);
	ubyte[32] sha = sha256Of(text);
	char[] encodedhash =  Base64.encode(sha);
	string ccMovel = ccMovelSign(AppId,filename,cast(string)encodedhash,PIN,UserId);
	writeln("ProcessID devolvido pela operação CCMovelSign: " ~ ccMovel);
	string OTP;
	OTP = readln.strip;
	string[] otpresult = ValidateOtp(OTP,ccMovel, AppId);
	if(otpresult[1] != "200")
	{
		writeln("Erro " ~otpresult[1] ~ ". " ~  otpresult[2]);

		exit(0);
	}

	writeln("Assinatura (em base 64) devolvida pela operação ValidateOtp: " ~ otpresult[0]);

}
///testa automaticamente a sequência de comandos GetCertificate, CCMovelSign e ValidateOtp
///verificando no final a assinatura, baseado na assinatura recebida, na hash gerada e na chave pública do certificado recebido
void TestAll(string UserId, string filename,string PIN)
{
	writeln("10% ... A contactar servidor SOAP CMD para operação GetCertificate");
    string[] certs = getCertificate(AppId,UserId);
		
    BIO *bio_mem1 = BIO_new(BIO_s_mem());
	BIO *bio_mem2 = BIO_new(BIO_s_mem());
	BIO *bio_mem3 = BIO_new(BIO_s_mem());
    
	BIO_puts(bio_mem1, cast(char*)certs[0]);
	BIO_puts(bio_mem2, cast(char*)certs[1]);
	BIO_puts(bio_mem3, cast(char*)certs[2]);
	X509 *certuser = PEM_read_bio_X509(bio_mem1,null,null,null);
    X509 *certca = PEM_read_bio_X509(bio_mem2,null,null,null);
	X509 *certroot = PEM_read_bio_X509(bio_mem3,null,null,null);
    BIO_free(bio_mem1);
	BIO_free(bio_mem2);
	BIO_free(bio_mem3);
	
	writeln("20% ... Certificado emitido para " ~ getCN(certuser) ~ 
          " pela Entidade de Certificação " ~ getCN(certca) ~
          " na hierarquia do " ~ getCN(certroot) );
	
	string text = readText(filename);
	writeln("30% ... Leitura do ficheiro " ~ filename);
	
	writeln("40% ... Geração de hash do ficheiro " ~filename);
	
    ubyte[32] sha = sha256Of(text);
	char[] encodedhash =  Base64.encode(sha);


	/*SHA256_CTX chazinho;
	auto sha = new ubyte[32];
	SHA256_Init(&chazinho);
	SHA256_Update(&chazinho,text.ptr,text.length);
	SHA256_Final(sha.ptr,&chazinho);
	char[] encodedhash = Base64.encode(sha);*/

    writeln(" 50% ... Hash gerada (em base64): " ~
         encodedhash);
	writeln("60% ... A contactar servidor SOAP CMD para operação CCMovelSign");
	string ccMovel = ccMovelSign(AppId,filename,cast(string)encodedhash,PIN,UserId);
	writeln("70% ... ProcessID devolvido pela operação CCMovelSign: " ~ ccMovel);
	
	writeln("80% ... A iniciar operação ValidateOtp");
	string OTP;
	writeln("Introduza o OTP recebido no seu dispositivo: ");
	OTP = readln.strip;
	writeln("90% ... A contactar servidor SOAP CMD para operação ValidateOtp");
	string[] otpresult = ValidateOtp(OTP,ccMovel, AppId);
	//otpresult[sig,code,msg]
	if(otpresult[1] != "200")
	{
		writeln("Erro " ~otpresult[1] ~ ". " ~  otpresult[2]);
		X509_free(certuser);
		X509_free(certca);
		X509_free(certroot);
		exit(0);
	}
	writeln("100% ... Assinatura (em base 64) devolvida pela operação ValidateOtp: " ~ otpresult[0]);
    writeln("110% ... A validar assinatura ..."  );

	ubyte[] decodedsig = Base64.decode(otpresult[0]);
	EVP_PKEY* pubkey =  X509_get_pubkey(certuser);
	RSA* rsa = RSA_new();
	rsa = EVP_PKEY_get1_RSA(pubkey);
	/*EVP_PKEY_free(pubkey);
	EVP_MD_CTX *mdctx = EVP_MD_CTX_new();
	
	if (EVP_DigestVerifyInit(mdctx,null, EVP_sha256(),null,pubkey)<=0) {
     exit(0);
  }
  if (EVP_DigestVerifyUpdate(mdctx, text.ptr, text.length) <= 0) {
    exit(0);
  }
  int AuthStatus = EVP_DigestVerifyFinal(mdctx, &decodedsig[0], decodedsig.length);*/
	ubyte[] textcast = cast(ubyte[]) text;
 	auto stuff = RSA_verify(NID_sha256,&textcast[0],cast(int)text.length,decodedsig.ptr,RSA_size(rsa),rsa);
	
	if(stuff == 1)
	{
		 writeln("Assinatura verificada com sucesso, baseada na assinatura recebida, na hash gerada e \n
          na chave pública do certificado de " ~ getCN(certuser));
	}
	else
	{
		writeln("Falha na verificação da assinatura");
	}
	X509_free(certuser);
	X509_free(certca);
	X509_free(certroot);
	RSA_free(rsa);
}


	///vai buscar o nome comum no certificado
	string getCN(X509 *cert)
	{	int last = -1;
		auto name = X509_get_subject_name(cert);
		X509_NAME_ENTRY* entry;
    	char* utf8;
		string data;
		 if (name != null) 
		 {
			last = X509_NAME_get_index_by_NID(name, NID_commonName, last);
			entry = X509_NAME_get_entry(name, last);
			auto common = X509_NAME_ENTRY_get_data(entry);
      		auto size = ASN1_STRING_to_UTF8(&utf8, common);
			data ~= utf8[0..size];

		 }

		 return data;
	}
