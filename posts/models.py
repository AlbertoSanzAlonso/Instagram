from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Usuario")
    image = models.ImageField(upload_to='posts_images/', verbose_name="Imagen")
    caption = models.TextField(max_length=500, blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    likes = models.ManyToManyField(User, related_name='liked_posts', verbose_name="Número de Likes")

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"{self.user.username} comment {self.post}"
    
# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'post')
#         verbose_name = 'Me gusta'
#         verbose_name_plural = 'Me gusta'

#     def __str__(self):
#         return f"{self.user} likes {self.post}"