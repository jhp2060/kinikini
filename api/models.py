from django.contrib.auth.models import AbstractUser
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "(" + str(self.pk) + ") " + str(self.name)

    class Meta:
        verbose_name_plural = "Organizations"


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    review_cnt = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return "(" + str(self.pk) + ") " + str(self.username)

    class Meta:
        verbose_name_plural = "Users"


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
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='cafeterias'
    )
    name = models.CharField(max_length=20)

    def __str__(self):
        return '(' + str(self.pk) + ") " + str(self.organization.name) + " " + str(self.name)


class Menu(models.Model):
    cafeteria = models.ForeignKey(
        Cafeteria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='menus'
    )
    TIME_CHOICES = (
        ("BREAKFAST", "BREAKFAST"),
        ("LUNCH", "LUNCH"),
        ("DINNER", "DINNER"),
    )
    time = models.CharField(
        max_length=10,
        choices=TIME_CHOICES,
        default=None,
    )
    date = models.DateField()

    def __str__(self):
        return str(self.cafeteria.name)+" "+str(self.date)+" "+self.time


class Dish(LikeMixinModel):
    menus = models.ManyToManyField(
        Menu,
        related_name='dishes',
    )
    name = models.CharField(max_length=20)
    is_new = models.BooleanField(default=True)
    recent_date = models.DateField(auto_now=True)
    frequency = models.IntegerField(default=1)
    is_bab_guk_kimchi = models.BooleanField(default=False)
    rating_sum = models.BigIntegerField(default=0)
    rating_count = models.BigIntegerField(default=0)

    class Meta:
        verbose_name_plural = "dishes"

    def avg_rating(self):
        return self.rating_sum / self.rating_count

    def __str__(self):
        return "(" + str(self.pk) + ") " + str(self.name)


class Review(LikeMixinModel):
    rating = models.IntegerField(default=0)
    written_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews',
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    comment = models.TextField(max_length=300, default="먹을만해요.")
    written_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default=None, blank=True)

    def is_already_written(self, writer, date):
        return (writer == self.written_by) and (date == self.written_at)


class FavoriteDish(models.Model):
    favored_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_dishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='favorite_dishes'
    )


class FavoriteCafeteria(models.Model):
    favored_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_cafeteria'
    )
    cafeteria = models.ForeignKey(
        Cafeteria,
        on_delete=models.CASCADE,
        related_name='favorite_cafeteria'
    )
