from text_unidecode import unidecode
from django.utils.text import slugify


def default_log():
    return {"state": 0}


def lang_dict_field():
    return {'ru': '', 'uz': ''}


def create_slug(instance):
    slug = instance.slug
    if slug is None or slug == "":
        slug = slugify(unidecode(instance.name['ru']))
    Klass = instance.__class__
    if instance.pk:
        qs_exists = Klass.objects.filter(slug=slug).exclude(id=instance.pk).exists()
    else:
        qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        slug = slugify("{}-{}".format(unidecode(instance.name['ru']), datetime.now().timestamp()))

    return slug
