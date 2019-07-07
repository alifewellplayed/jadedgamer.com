from django.db import models
from django.core.cache import cache
from django.conf import settings

from coreExtend.models import Account
from aggregator.models import FeedItem

BLOCKED_IPS_LIST = 'external-link:blocked-ips'

class BlockedManager(models.Manager):
    def get_ips(self):
        """
        Returns a cached list of ip addresses
        """
        result = cache.get(BLOCKED_IPS_LIST, None)
        if not result:
            result = self.values_list('ip_addr', flat=True)
            cache.set(BLOCKED_IPS_LIST, result, 60*60*24) # 1 day
        return result

class BlockedIp(models.Model):
    name = models.CharField(max_length=128, blank=True)
    ip_addr = models.GenericIPAddressField(null=True)
    objects = BlockedManager()

    def __unicode__(self):
        return self.ip_addr

    def save(self, *args, **kwargs):
        cache.delete(BLOCKED_IPS_LIST)
        super(BlockedIp, self).save(*args, **kwargs)


class LinkClick(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    link = models.ForeignKey(FeedItem, related_name='clicks', null=True, on_delete=models.CASCADE)
    referer = models.CharField(max_length=512)
    user_agent = models.CharField(max_length=1024, null=True)
    ip_addr = models.GenericIPAddressField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def store(self, request):
        #Update params based on Request object
        ip_addr = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT','')

        if ip_addr in BlockedIp.objects.get_ips():
            # If it's a blocked IP or user agent, dont do anything
            return None

        user = None
        if request.user.is_authenticated():
            user = request.user

        self.user = user
        self.referer = request.META.get('HTTP_REFERER','')
        self.user_agent = user_agent
        self.ip_addr = ip_addr

        try:
            self.save()
        except:
            pass

    class Meta:
        ordering = ("-pub_date",)
        unique_together = ("link", "ip_addr")
