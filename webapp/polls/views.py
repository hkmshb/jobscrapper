from django.http import HttpResponse


def is_geopy_installed():
    """Returns True if geopy is installed otherwise false.
    """
    try:
        import geopy
        return True
    except ModuleNotFoundError:
        return False


def index(request):
    is_installed = is_geopy_installed()
    data = f"""
        <div style="text-align: center; padding: 100px">
            <h1>Hello, World!</h1>
            <p>
                You're at the polls app index. <br/>
                The setup started up successfully!
            </p>
            <p> ... </p>
            <p>
                Is geopy installed? {is_installed}
            </p>
        </did>
    """
    return HttpResponse(data)
