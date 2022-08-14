from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# cвязь «один к одному» с встроенной моделью пользователей User;+
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

class Autor(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAutor = models.SmallIntegerField(default=0)

#  #Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
# Он состоит из следующего:
# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора
    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        comRat = self.autorUser.comment_set.aggregate(comRating=Sum('rating'))
        cRat = 0
        cRat += comRat.get('comRating')

        self.ratingAutor = pRat * 3 + cRat
        self.save()

sport = 's'
politics = 'p'
education = 'e'
art = 'a'

TOPICS = [
    (sport, 'Спорт'),
    (politics, 'политика'),
    (education, 'образование'),
    (art, 'искусство')
]

class Category(models.Model):
    name = models.CharField(max_length=225, choices=TOPICS, unique=True)

# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:+
# связь «один ко многим» с моделью Author;+
# поле с выбором — «статья» или «новость»;+
# автоматически добавляемая дата и время создания;+
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);+
# заголовок статьи/новости;+
# текст статьи/новости;+
# рейтинг статьи/новости.


class Post(models.Model):
    PostAutor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    article = 'AR'
    news = 'NW'
    ARTICLEORNEWS = [
        (article, 'статья'),
        (news, 'сатья')
    ]
    Choise = models.CharField(max_length=2, choices=ARTICLEORNEWS, default=article)
    timeCreation = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    _postcategory = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'



class PostCategory(models.Model):
    _Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    _Category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Модель Comment
# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.
class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    timeCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()