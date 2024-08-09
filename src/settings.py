BOT_NAME = 'web_scraper'

SPIDER_MODULES = ['src.infra.adapters']
NEWSPIDER_MODULE = 'src.infra.adapters'

DOWNLOAD_TIMEOUT = 600
CONCURRENT_REQUESTS = 1
RETRY_TIMES = 10
