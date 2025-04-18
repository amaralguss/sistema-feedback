from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina, Feedback
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm, RegistroForm
from django.db.models import Avg
from django.contrib.auth import login


def profile(request):
    return render(request, 'profile.html')


def home(request):
    return render(request, 'avaliacoes/home.html')


def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        media = Feedback.objects.filter(disciplina=disciplina).aggregate(Avg('nota'))['nota__avg']
        disciplina.media = media if media else 'Ainda não avaliada'
    return render(request, 'avaliacoes/lista_disciplinas.html', {'disciplinas': disciplinas})


def detalhes_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    feedbacks = Feedback.objects.filter(disciplina=disciplina)
    media = feedbacks.aggregate(Avg('nota'))['nota__avg']
    media = media if media else 'Ainda não avaliada'

    usuario_avaliou = False
    if request.user.is_authenticated:
        usuario_avaliou = feedbacks.filter(aluno=request.user).exists()

    return render(request, 'avaliacoes/detalhes_disciplina.html', {
        'disciplina': disciplina,
        'feedbacks': feedbacks,
        'media': media,
        'usuario_avaliou': usuario_avaliou
    })


@login_required
def avaliar_disciplina(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)

    if Feedback.objects.filter(disciplina=disciplina, aluno=request.user).exists():
        return redirect('detalhes_disciplina', id=disciplina.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.aluno = request.user
            feedback.disciplina = disciplina
            feedback.save()
            return redirect('detalhes_disciplina', id=disciplina.id)
    else:
        form = FeedbackForm()
    return render(request, 'avaliacoes/avaliar_disciplina.html', {'form': form, 'disciplina': disciplina})


@login_required
def editar_feedback(request, id, feedback_id):
    disciplina = get_object_or_404(Disciplina, id=id)
    feedback = get_object_or_404(Feedback, id=feedback_id, aluno=request.user)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('detalhes_disciplina', id=disciplina.id)
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'avaliacoes/editar_feedback.html', {'form': form, 'disciplina': disciplina})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'avaliacoes/registro.html', {'form': form})
