from typing import Callable, Awaitable

from dishka.integrations.base import wrap_injection


def inject_on_process_result(func: Callable) -> Callable:
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[2].middleware_data['dishka_container'],
        is_async=True,
        remove_depends=True,
     )



def inject_getter(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p["dishka_container"],
        is_async=True,
    )


def inject_on_click(func: Callable) -> Awaitable:
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[2].middleware_data["dishka_container"],
        is_async=True,
        remove_depends=True,
     )
