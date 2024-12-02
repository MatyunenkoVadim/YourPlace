from starlette.staticfiles import StaticFiles


class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if path.endswith(".html"):
            response.headers["Content-Type"] = "text/html; charset=utf-8"
        elif path.endswith(".js"):
            response.headers["Content-Type"] = "application/javascript"
        return response
