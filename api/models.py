from django.contrib.auth.models import AbstractUser
from django.db import models


class BelongsTo(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "("+str(self.pk)+") "+str(self.name)

    class Meta:
        verbose_name_plural = "Schools/Companies"


class User(AbstractUser):
    belongs_to = models.ForeignKey(
        BelongsTo,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    review_cnt = models.IntegerField(default=0)
    level = models.IntegerField(default=1)


class LikeMixinModel(models.Model):
    liker_set = models.ManyToManyField(
        User,
        related_name='liked_%(class)s_set',
        blank=True,
    )

    class Meta:
        abstract = True

    def count_like(self):
        return self.liker_set.count()

    def is_liked_by(self, user):
        return self.liker_set.filter(pk=user.pk).exists()

    def toggle_like(self, user):
        liked = self.is_liked_by(user)
        if liked:
            self.liker_set.remove(user)
        else:
            self.liker_set.add(user)
        return not liked


class Cafeteria(models.Model):
    belongs_to = models.ForeignKey(
        BelongsTo,
        on_delete=models.CASCADE,
        related_name='cafeterias'
    )
    name = models.CharField(max_length=20)

    def __str__(self):
        return '('+str(self.pk)+") "+str(self.belongs_to.name)+" "+str(self.name)


class Menu(models.Model):
    cafeteria = models.ForeignKey(
        Cafeteria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='menus'
    )
    TIME_CHOICES=(
        ("BREAKFAST", "BREAKFAST"),
        ("LUNCH", "LUNCH"),
        ("DINNER", "DINNER"),
    )
    time = models.CharField(
        max_length=10,
        choices=TIME_CHOICES,
        default=None,
    )
    def __str__(self):
        return '('+str(self.pk)+") "+str(self.cafeteria.name)+"의 메뉴"



class Dish(LikeMixinModel):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='dishes'
    )
    name = models.CharField(max_length=20)
    is_new = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    recent_date = models.DateField(auto_now=True)
    is_bab_guk_kimchi = models.BooleanField(default=False)
    rating_sum = models.BigIntegerField(default=0)
    rating_count = models.BigIntegerField(default=0)
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "dishes"

    def __str__(self):
        return "("+str(self.pk)+") "+str(self.menu.cafeteria.name)+" "+str(self.name)


class Review(LikeMixinModel):
    written_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    comment = models.TextField(max_length=300, default=None)
    written_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default=None)

    def is_already_written(self, writer, date):
        return (writer == self.written_by) and (date == self.written_at)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    review = models.OneToOneField(
        Review,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rating'
    )
    rated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ratings'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

class Wish(models.Model):
    wished_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='wishes'
    )

