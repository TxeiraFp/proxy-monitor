import requests
from mitmproxy import http
import time
import json
import gzip


BACKEND_URL = "http://localhost:3007/api/v1/capture"


MAX_BODY = 5000000


CONTENT_ALLOWED = [
    "application/json",
    "application/x-www-form-urlencoded",
    "text/plain",
    "multipart/form-data"
]


IGNORE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".css",
    ".js",
    ".woff",
    ".woff2",
    ".ttf",
    ".map",
    ".mp4",
    ".webp"
]


HEADERS_SAVE = [
    "authorization",
    "content-type",
    "user-agent",
    "cookie",
    "set-cookie",
    "referer",
    "origin"
]



def limpar_texto(valor):

    if not valor:
        return ""

    if isinstance(valor, bytes):

        valor = valor.decode(
            "utf-8",
            errors="ignore"
        )


    return (
        valor
        .replace("\x00", "")
        .replace("\u0000", "")
    )



def capturar_tipo(content_type):

    if not content_type:
        return False

    content_type = content_type.lower()

    return any(
        x in content_type
        for x in CONTENT_ALLOWED
    )



def limpar_body(data, headers):

    if not data:
        return ""


    encoding = headers.get(
        "content-encoding",
        ""
    )


    try:

        if "gzip" in encoding.lower():

            data = gzip.decompress(data)


    except:

        return "<gzip invalido>"


    try:

        texto = data.decode(
            "utf-8",
            errors="ignore"
        )


        texto = limpar_texto(texto)


        if len(texto) > MAX_BODY:
            texto = texto[:MAX_BODY]


        try:

            obj = json.loads(texto)

            return json.dumps(
                obj,
                indent=2,
                ensure_ascii=False
            )


        except:

            return texto


    except:

        return ""





def ignorar_url(url):

    url = url.lower()

    return any(
        url.endswith(ext)
        for ext in IGNORE_EXTENSIONS
    )





def pegar_headers(headers):

    lista = []


    for k,v in headers.items():

        if k.lower() in HEADERS_SAVE:

            lista.append(
                {
                    "key": k,
                    "value": limpar_texto(v)
                }
            )


    return lista





def pegar_cookies(cookies):

    resultado=[]


    for k,v in cookies.items():

        resultado.append(
            {
                "key":k,
                "value":limpar_texto(v)
            }
        )


    return resultado





def enviar_backend(data):

    try:

        requests.post(
            BACKEND_URL,
            json=data,
            timeout=5
        )


    except Exception as e:

        print(
            "Erro backend:",
            e
        )







class Capture:


    def request(self, flow:http.HTTPFlow):


        # SOMENTE POST

        if flow.request.method != "POST":

            flow.metadata["skip"] = True
            return



        if ignorar_url(
            flow.request.pretty_url
        ):

            flow.metadata["skip"] = True
            return



        flow.metadata["inicio"] = time.time()



        ct = flow.request.headers.get(
            "content-type",
            ""
        )


        if capturar_tipo(ct):

            flow.metadata["request_body"] = limpar_body(
                flow.request.content,
                flow.request.headers
            )

        else:

            flow.metadata["request_body"] = ""







    def response(self, flow:http.HTTPFlow):


        if flow.metadata.get("skip"):

            return



        if flow.request.method != "POST":

            return



        tempo = (
            time.time()
            -
            flow.metadata.get(
                "inicio",
                time.time()
            )
        )


        request_body = flow.metadata.get(
            "request_body",
            ""
        )



        response_ct = flow.response.headers.get(
            "content-type",
            ""
        )


        response_body=""


        if capturar_tipo(response_ct):

            response_body = limpar_body(
                flow.response.content,
                flow.response.headers
            )




        dados={


            "clientIp":
                flow.client_conn.address[0],


            "scheme":
                flow.request.scheme,


            "host":
                flow.request.host,


            "port":
                flow.request.port,


            "method":
                flow.request.method,


            "url":
                flow.request.pretty_url.split("?")[0],


            "path":
                flow.request.path.split("?")[0],


            "query":
                "",



            "httpVersion":
                flow.request.http_version,



            "requestBody":
                request_body,


            "responseBody":
                response_body,


            "statusCode":
                flow.response.status_code,


            "requestSize":
                len(flow.request.content),


            "responseSize":
                len(flow.response.content),



            "durationMs":
                round(
                    tempo*1000,
                    2
                ),



            "contentType":
                response_ct,



            "tls":
                flow.request.scheme=="https",



            "headers":
                [
                    {
                        "key":x,
                        "value":limpar_texto(y),
                        "type":"request"
                    }

                    for x,y in flow.request.headers.items()

                    if x.lower() in HEADERS_SAVE
                ],



            "cookies":
                pegar_cookies(
                    flow.request.cookies
                )

        }



        enviar_backend(dados)



        print(
            "POST capturado:",
            flow.request.pretty_url,
            flow.response.status_code
        )





addons=[
    Capture()
]
