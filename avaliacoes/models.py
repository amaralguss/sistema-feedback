from django.db import models
from django.contrib.auth.models import User

class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    
    def __str__(self):
        return self.nome

class Feedback(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    anonimo = models.BooleanField(default=False)

    def __str__(self):
        return f'Feedback de {self.aluno} para {self.disciplina}'
