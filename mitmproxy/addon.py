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
        texto = content.decode("utf-8", errors="replace")

        try:
            return json.dumps(
                json.loads(texto),
                indent=2,
                ensure_ascii=False
            )
        except:
            return texto

    except Exception:
        return "<dados binários>"


def enviar_backend(dados):
    try:
        requests.post(
            BACKEND_URL,
            json=dados,
            timeout=3
        )

    except Exception as e:
        print("Erro enviando para backend:", e)


class Capture:

    def request(self, flow: http.HTTPFlow):

        flow.metadata["inicio"] = time.time()

        flow.metadata["request_body"] = limpar_body(
            flow.request.content
        )


    def response(self, flow: http.HTTPFlow):

        tempo = 0

        if "inicio" in flow.metadata:
            tempo = round(
                time.time() - flow.metadata["inicio"],
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
            "method": flow.request.method,
            "url": flow.request.pretty_url,
	    "scheme": flow.request.scheme,
            "status": flow.response.status_code,
            "tempo": tempo,
            "requestBody": request_body,
            "responseBody": response_body
        }


        enviar_backend(dados)


        print("\n" + "=" * 60)

        print(f"{flow.request.method} {flow.request.pretty_url}")

        print(f"Status: {flow.response.status_code}")

        print(f"Tempo: {tempo}s")


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
