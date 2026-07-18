import requests
from mitmproxy import http
import time
import json


MAX_BODY = 10000

BACKEND_URL = "http://localhost:3007/capture"


def limpar_body(content):

    if not content:
        return ""

    try:

        texto = content.decode(
            "utf-8",
            errors="replace"
        )

        try:
            obj = json.loads(texto)

            return json.dumps(
                obj,
                indent=2,
                ensure_ascii=False
            )[:MAX_BODY]

        except Exception:
            return texto[:MAX_BODY]

    except Exception:
        return "<dados binários>"


def headers_dict(headers):

    return [
        {
            "key": k,
            "value": v
        }
        for k, v in headers.items()
    ]


def cookies_dict(cookies):

    try:
        return dict(cookies)

    except Exception:
        return {}


def enviar_backend(dados):

    try:

        r = requests.post(
            BACKEND_URL,
            json=dados,
            timeout=5
        )

        if r.status_code >= 400:
            print(
                "Backend respondeu:",
                r.status_code,
                r.text[:200]
            )

    except Exception as e:

        print(
            "Erro enviando para backend:",
            e
        )


class Capture:


    def request(self, flow: http.HTTPFlow):

        flow.metadata["inicio"] = time.time()


        flow.metadata["request_body"] = limpar_body(
            flow.request.content
        )


    def response(self, flow: http.HTTPFlow):


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


        response_body = limpar_body(
            flow.response.content
        )


        dados = {


            "clientIp":
                flow.client_conn.address[0],


            "serverIp":
                flow.server_conn.address[0]
                if flow.server_conn
                else None,


            "scheme":
                flow.request.scheme,


            "host":
                flow.request.host,


            "port":
                flow.request.port,


            "method":
                flow.request.method,


            "url":
                flow.request.pretty_url,


            "path":
                flow.request.path,


            # CORREÇÃO PRINCIPAL
            "query":
                dict(flow.request.query),


            "httpVersion":
                flow.request.http_version,


            "requestBody":
                request_body,


            "responseBody":
                response_body,


            "statusCode":
                flow.response.status_code,


            "requestSize":
                len(flow.request.content or b""),


            "responseSize":
                len(flow.response.content or b""),


            "durationMs":
                tempo * 1000,


            "contentType":
                flow.response.headers.get(
                    "content-type",
                    ""
                ),


            "tls":
                flow.request.scheme == "https",


            "requestHeaders":
                headers_dict(
                    flow.request.headers
                ),


            "responseHeaders":
                headers_dict(
                    flow.response.headers
                ),


            "cookies":
                cookies_dict(
                    flow.request.cookies
                )

        }


        enviar_backend(dados)


        print("\n" + "=" * 60)

        print(
            f"{flow.request.method} "
            f"{flow.request.pretty_url}"
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


        if request_body:

            print("\nREQUEST BODY:")
            print(request_body)


        if response_body:

            print("\nRESPONSE BODY:")
            print(response_body)


        print("=" * 60)



addons = [
    Capture()
]
