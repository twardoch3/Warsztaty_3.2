from .forms import SearchFrom
def my_cp(request):
    ctx = {
    'form_search': SearchFrom()
    }
    return ctx