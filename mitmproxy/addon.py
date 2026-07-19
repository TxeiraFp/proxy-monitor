import requests
from mitmproxy import http
import time
import json


MAX_BODY = 10000


BACKEND_URL = "http://localhost:3007/api/v1/capture"



HEADERS_IMPORTANTES = [

    "authorization",
    "content-type",
    "user-agent",
    "cookie",
    "set-cookie",
    "referer",
    "origin"

]



TIPOS_BODY = [

    "application/json",
    "application/x-www-form-urlencoded",
    "text/plain"

]



EXTENSOES_IGNORAR = [

    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".css",
    ".woff",
    ".woff2",
    ".ttf",
    ".map",
    ".mp4",
    ".webp"

]


def limpar_null(texto):

    if not texto:
        return ""


    return texto.replace(
        "\x00",
        ""
    )


def limpar_body(content):

    if not content:
        return ""


    try:

        texto = content.decode(
            "utf-8",
            errors="replace"
        )


        texto = texto.replace(
            "\x00",
            ""
        )


        try:

            return json.dumps(
                json.loads(texto),
                indent=2,
                ensure_ascii=False
            )


        except:

            return texto[:MAX_BODY]


    except Exception:

        return "<dados binarios>"


def capturar_body(content_type):

    if not content_type:

        return False


    content_type = content_type.lower()


    return any(

        tipo in content_type

        for tipo in TIPOS_BODY

    )







def ignorar_url(url):

    url = url.lower()


    return any(

        url.endswith(ext)

        for ext in EXTENSOES_IGNORAR

    )







def pegar_headers(headers):

    resultado = []


    for key,value in headers.items():


        if key.lower() in HEADERS_IMPORTANTES:


            resultado.append({

                "key": key,

                "value": value

            })


    return resultado


def pegar_cookies(cookies):

    resultado = []


    for key,value in cookies.items():

        resultado.append({

            "key": key,

            "value": value

        })


    return resultado



def enviar_backend(dados):

    try:


        response = requests.post(

            BACKEND_URL,

            json=dados,

            timeout=3

        )


        print(

            "BACKEND:",

            response.status_code

        )



    except Exception as e:


        print(

            "Erro enviando para backend:",

            e

        )








class Capture:



    def request(self, flow: http.HTTPFlow):


        flow.metadata["inicio"] = time.time()



        content_type = flow.request.headers.get(

            "content-type",

            ""

        )



        if capturar_body(content_type):


            flow.metadata["request_body"] = limpar_body(

                flow.request.content

            )


        else:

            flow.metadata["request_body"] = ""









    def response(self, flow: http.HTTPFlow):


        if ignorar_url(

            flow.request.pretty_url

        ):

            return





        inicio = flow.metadata.get(

            "inicio",

            time.time()

        )



        tempo = round(

            time.time() - inicio,

            3

        )




        request_body = flow.metadata.get(

            "request_body",

            ""

        )





        content_type = flow.response.headers.get(

            "content-type",

            ""

        )





        response_body = ""



        if capturar_body(content_type):


            response_body = limpar_body(

                flow.response.content

            )






        dados = {


            "clientIp": flow.client_conn.address[0],


            "scheme": flow.request.scheme,


            "host": flow.request.host,


            "port": flow.request.port,



            "method": flow.request.method,


            "url": flow.request.pretty_url,


            "path": flow.request.path,


            "query": str(flow.request.query),



            "httpVersion": flow.request.http_version,



            "requestBody": request_body,


            "responseBody": response_body,



            "statusCode": flow.response.status_code,



            "requestSize": len(
                flow.request.content or b""
            ),


            "responseSize": len(
                flow.response.content or b""
            ),



            "durationMs": tempo * 1000,



            "contentType": content_type,



            "tls": flow.request.scheme == "https",



            "headers": [

    {
        "key": k,
        "value": v,
        "type": "request"
    }

    for k,v in flow.request.headers.items()

],



            "cookies": pegar_cookies(

                flow.request.cookies

            )

        }





        enviar_backend(dados)




        print("\n" + "="*60)

        print(

            flow.request.method,

            flow.request.pretty_url

        )

        print(

            "Status:",

            flow.response.status_code

        )

        print(

            "Tempo:",

            tempo,

            "s"

        )


        print("="*60)






addons = [

    Capture()

]
