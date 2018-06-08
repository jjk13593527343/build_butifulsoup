# coding:utf-8

DATA_PATH = 'data'
PREPARE_FOR_DIRS = ['log']

CFG = {
    'sleep_time': 6,
    'run_sleep_time': 4,
    's3_bucket': 'api-saic',
    'components': [
        {
            'name': 'reaper',
            'class_name': 'scpy2.components.requests_session.RequestsSession',
            'cfg': {
                'pries'
            }
        }
    ],
    "crawl_processor": {
        "class_name": "demo_crawler_processor.DemoCrawlerProcessor",
    }
}