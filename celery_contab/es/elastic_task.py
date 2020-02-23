from celery_contab.celery import cel


@cel.task
def create_index():
    pass
