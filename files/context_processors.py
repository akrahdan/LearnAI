from .models import S3File


def avatar_processor(request):
    if request.user.is_authenticated:
        user = request.user
        qs = S3File.objects.filter(user=user)
        if qs.exists():
            avatar = qs.last().get_download_url()
            return {'avatar': avatar}
        return {}
    return  {}