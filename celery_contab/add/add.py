from celery_contab.celery import cel


@cel.task
def add(x, y):
    s = x + y
    print(s)
    return s
