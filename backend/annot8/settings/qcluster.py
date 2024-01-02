Q_CLUSTER = {
    'name': 'annot8',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Queue Tasks',
    'bulk': 10,
    'orm': 'default',
    'django_redis': 'default'
}
