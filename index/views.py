from django.shortcuts import render
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

from django.views.generic import View
from django.contrib.auth.decorators import login_required ,permission_required
from django.utils.decorators import method_decorator

class Index(LoginRequiredMixin,View):
    # @method_decorator(permission_required('user.manager_permission'))
    def get(self, request):
        return render(request, 'index/index.html')

