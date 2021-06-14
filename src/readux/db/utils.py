import random
import string
from django.utils.text import slugify


def get_random_string(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = get_random_string(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return get_unique_slug(instance)
    return key

def get_unique_slug(instance, new_slug=None, size=10, max_size=30):
    title = instance.title
    if new_slug is None:
        """
        Default
        """
        slug = slugify(title)
    else:
        """
        Recursive
        """
        slug = new_slug
    slug = slug[:max_size]
    Klass = instance.__class__ # Course, Category
    parent = None
    try:
        parent = instance.parent
    except:
        pass
    if parent is not None:
        qs = Klass.objects.filter(parent=parent, slug=slug) # smaller
    else:
        qs = Klass.objects.filter(slug=slug) # larger
    if qs.exists():
        new_slug = slugify(title) + get_random_string(size=size)
        return get_unique_slug(instance, new_slug=new_slug)
    return slug


def generate_lecture_id(instance):
    """
    This is for a Django project with an order_id field
    """
    lecture_new_id = get_random_string()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(lecture_id=lecture_new_id).exists()
    if qs_exists:
        return get_unique_slug(instance)
    return lecture_new_id

def unique_purchase_id_generator(instance):
    """
    This is for a Django project with an order_id field
    """
    purchase_new_id = get_random_string()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(purchase_id=purchase_new_id).exists()
    if qs_exists:
        return get_unique_slug(instance)
    return purchase_new_id
