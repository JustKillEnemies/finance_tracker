from .utils import menu
from .models import ContextMenu


def get_context_menu(request):

    menu = ContextMenu.objects.all().order_by('order')
    return {"mainmenu": menu}
