from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.signals import user_logged_in,user_logged_out

# Create your models here.


def upload_location_post(object,filename):
    return "posts/%s/%s" %(object.Author.pk,filename)

def upload_location_profile_pic(object,filename):
    return "profile_pics/%s/%s" %(object.Author.pk,filename)

class PostModel(models.Model):
    Author          =models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    title           =models.CharField(max_length=120,default='')
    slug            =models.SlugField(unique=True,null=True,blank=True)
    content         =models.TextField(max_length=1024, default='')
    likes           =models.ManyToManyField(User, default=0, related_name='postlikes')
    image           =models.ImageField(upload_to=upload_location_post,null=True,)
    timestamp       =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Posts:postdetail',kwargs={'slug':self.slug})

    def get_like_url(self):
        return reverse('Posts:like-toggle',kwargs={'slug':self.slug})

class AuthorDetailModel(models.Model):
    Author          = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name       =models.CharField(max_length=56, null=True,blank=True)
    work            =models.TextField(max_length=512,default='',null=True)
    address         =models.TextField(max_length=512,default='',null=True)
    profile_pic     =models.ImageField(upload_to=upload_location_profile_pic,null=True,blank=True)
    author_bio      =models.TextField(max_length=512,default='',null=True)

    def __str__(self):
        return self.Author.username
    
    def save(self,*args,**kwargs):
        self.full_name = self.Author.get_full_name()
        super(AuthorDetailModel,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('Posts:authordetail',kwargs={'pk':self.pk})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = PostModel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=PostModel)

class CommentsModel(models.Model):
    Author          =models.ForeignKey(User,default=1)
    content         =models.TextField(max_length=258,null=True,blank=True)
    timestamp       =models.DateTimeField(auto_now_add=False,auto_now=True,null=True)

    def __str__(self):
        return self.Author.first_name

class Post_views(models.Model):
    entry = models.ForeignKey(PostModel,related_name='post_views')
    ip= models.CharField(max_length=40)
    session=models.CharField(max_length=40,null=True)
    created =models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.entry.Author

    class Meta:
        verbose_name_plural = "Post_views"    
    
class LoggedUser(models.Model):
    user = models.ForeignKey(User, primary_key=True)

    def __unicode__(self):
        return self.user.username

    def login_user(sender, request, user, **kwargs):
        LoggedUser(user=user).save()

    def logout_user(sender, request, user, **kwargs):
        try:
            u = LoggedUser.objects.get(user=user)
            u.delete()
        except LoggedUser.DoesNotExist:
            pass

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)