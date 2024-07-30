from typing import Any
from datetime import datetime

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils import timezone

from .models import Board, List, Card
from .forms import ListForm, BoardForm, CardForm

import pytz



@method_decorator(never_cache, name="dispatch")
class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = "board_list.html"
    context_object_name = "boards"
    login_url = "/login/"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


@method_decorator(never_cache, name="dispatch")
class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "board_detail.html"
    context_object_name = "board"
    login_url = "/login/"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except:
            return None

    def get(self, request, *args, **kwargs):
        board = self.get_object()
        if not board:
            return redirect("board_list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board = self.get_object()
        context["lists"] = board.lists.prefetch_related("cards")
        context["list_form"] = ListForm()
        context["card_form"] = CardForm()
        print(timezone.now())
        context["timezone_now"] = timezone.now()
        return context
    

    def post(self, request, *args, **kwargs):
        board = self.get_object()
        if "delete_board" in request.POST:
            board.delete()
            return redirect("board_list")
        return super().post(request, *args, **kwargs)


@method_decorator(never_cache, name="dispatch")
class CreateBoardView(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request):
        form = BoardForm()
        return render(request, "create_board.html", {"form": form})

    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect("board_detail", pk=board.pk)
        return render(request, "create_board.html", {"form": form})


class ListView(LoginRequiredMixin, View):

    login_url = "/login/"

    def post(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        form = ListForm(request.POST)
        if form.is_valid():
            list_instance = form.save(commit=False)
            list_instance.board = board
            list_instance.save()
            return redirect("board_detail", pk=board.pk)
        return redirect("board_detail", pk=board.pk)


class CardView(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request, list_id):
        form = CardForm()
        list_instance = List.objects.get(pk=list_id)
        return render(
            request,
            "create_card.html",
            {"form": form, "list_id": list_id, "list": list_instance},
        )

    def post(self, request, list_id):
        list_instance = List.objects.get(pk=list_id)
        form = CardForm(request.POST)

        if "mark_completed" in request.POST:
            card = get_object_or_404(Card, pk=request.POST.get("card_id"))
            card.completed = True
            card.save()
            return redirect("board_detail", pk=list_instance.board.pk)

        if form.is_valid():
            card = form.save(commit=False)
            card.list = list_instance
            card.start_time = request.POST.get("start_time")
            card.end_time = request.POST.get("end_time")
            card.save()
            return redirect("board_detail", pk=list_instance.board.pk)
        return render(request, "create_card.html", {"form": form, "list_id": list_id})


@method_decorator(never_cache, name="dispatch")
class DeleteCardView(LoginRequiredMixin, View):

    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        card = get_object_or_404(Card, pk=kwargs["pk"])
        if "delete_card" in request.POST:
            board_pk = card.list.board.pk
            card.delete()
            return redirect("board_detail", pk=board_pk)
        return redirect("board_detail", pk=card.list.board.pk)


@method_decorator(never_cache, name="dispatch")
class DeleteListView(LoginRequiredMixin, View):

    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        list_instance = get_object_or_404(List, pk=kwargs["pk"])
        if "delete_list" in request.POST:
            board_pk = list_instance.board.pk
            list_instance.delete()
            return redirect("board_detail", pk=board_pk)
        return redirect("board_detail", pk=list_instance.board.pk)
