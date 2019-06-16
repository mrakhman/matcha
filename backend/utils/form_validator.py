from werkzeug.exceptions import BadRequest


def check_fields(data: dict, scheme: dict):
    ex = BadRequest()
    if not data:
        ex.description = "Body is empty or wrong content type"
        raise ex

    for name, props in scheme.items():
        if props['default']:
            data.setdefault(name, props["default"])

        if props['required']:
            if not data.get(name):
                ex.description = f"{name} is required"
                raise ex
            if props['type'] and type(data.get(name)) != props['type']:
                ex.description = f"{name} type is not {props['type']}"
                raise ex

        if props['validator'] and not props['validator'](data.get(name)):
            ex.description = f"{name}({data.get(name)}) did not pass validator"
            raise ex
