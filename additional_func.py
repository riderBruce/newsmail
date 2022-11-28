import time


def time_checker(func):
    def inner_func(*args, **kwargs):
        start = time.time()
        returned_value = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        print(f'>>> {str(func.__name__)} : 총 걸린 시간은 {duration} 초 입니다.')
        return returned_value
    return inner_func
