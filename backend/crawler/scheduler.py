from celery import Celery
from celery.schedules import crontab

from config import get_settings

settings = get_settings()
celery_app = Celery('yeg-shadow', broker=settings.redis_url, backend=settings.redis_url)

celery_app.conf.beat_schedule = {
    'full-crawl-shopify': {
        'task': 'crawler.tasks.crawl_shopify_stores',
        'schedule': crontab(hour='*/6'),
    },
    'full-crawl-woocommerce': {
        'task': 'crawler.tasks.crawl_woocommerce_stores',
        'schedule': crontab(hour='*/12'),
    },
    'enrichment-pipeline': {
        'task': 'enrichment.tasks.enrich_new_products',
        'schedule': crontab(minute='*/30'),
    },
}
