"""
Этот модуль определяет класс CustomStaticFiles, который расширяет функциональность
стандартного StaticFiles для обработки статических файлов с пользовательскими заголовками.

Классы:
- CustomStaticFiles: Класс для обслуживания статических файлов с измененными заголовками Content-Type.

Зависимости:
- Использует Starlette для работы со статическими файлами.

Контекст:
Этот файл используется для настройки обслуживания статических файлов в приложении,
позволяя изменять заголовки Content-Type для определенных типов файлов.
"""

from starlette.staticfiles import StaticFiles


class CustomStaticFiles(StaticFiles):
    """
    Класс для обслуживания статических файлов с измененными заголовками Content-Type.
    """

    async def get_response(self, path: str, scope):
        """
        Возвращает ответ для запрашиваемого статического файла с измененными заголовками Content-Type.

        Параметры:
        - path: Путь к запрашиваемому файлу.
        - scope: Контекст запроса.

        Возвращает:
        - Ответ с измененными заголовками Content-Type для HTML и JavaScript файлов.
        """
        response = await super().get_response(path, scope)
        if path.endswith(".html"):
            response.headers["Content-Type"] = "text/html; charset=utf-8"
        elif path.endswith(".js"):
            response.headers["Content-Type"] = "application/javascript"
        return response
