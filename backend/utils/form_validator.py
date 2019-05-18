from werkzeug.exceptions import BadRequest


def check_fields(data, scheme):
    ex = BadRequest()
    if not data:
        ex.description = "Body is empty or wrong content type"
        raise ex

    for name, props in scheme.items():
        if props['required'] and not data.get(name):
            ex.description = f"{name} is required"
            raise ex

        if props['validator'] and not props['validator'](data.get(name)):
            ex.description = f"{name}({data.get(name)}) did not pass validator"
            raise ex
