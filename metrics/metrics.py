from prometheus_client import Counter

MAIN_LOOP_EXCEPTION = Counter("main_loop_exception_counter", "Total number of main loop exceptions")
MAIN_LOOP_TICKS = Counter("main_loop_ticks_counter", "Total number of scans since loop starts")
