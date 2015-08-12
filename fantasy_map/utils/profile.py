import cProfile
import pstats


def profile(func):
    """Decorator for run function profile"""
    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        p = pstats.Stats(profile_filename)
        p.sort_stats('time').print_stats(10)
        return result
    return wrapper
