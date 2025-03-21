from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    """
    Representa uma sala de bate-papo no sistema.

    Attributes:
        name (str): O nome da sala de bate-papo (máximo de 20 caracteres).
        slug (str): Identificador único da sala, usado nas URLs (máximo de 100 caracteres).
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        """
        Retorna uma representação em string da sala.

        Returns:
            str: Nome da sala e seu identificador único.
        """
        return "Room : "+ self.name + " | Id : " + self.slug


class Message(models.Model):
    """
    Representa uma mensagem enviada em uma sala de bate-papo.

    Attributes:
        user (User): O usuário que enviou a mensagem.
        content (str): O conteúdo da mensagem.
        room (Room): A sala em que a mensagem foi enviada.
        created_on (datetime): Data e hora em que a mensagem foi criada.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna uma representação em string da mensagem.

        Returns:
            str: Conteúdo da mensagem.
        """
        return "Message is :- "+ self.content