from django.http import HttpResponse


def index(request):
    data = """
        <div style="text-align: center; padding: 100px">
            <h1>Hello, World!</h1>
            <p>
                You're at the polls app index. <br/>
                The setup started up successfully!
            </p>
        </did>
    """
    return HttpResponse(data)
