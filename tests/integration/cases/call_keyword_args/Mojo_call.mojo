def main():
    var throttler = object()
    fn print(a: object): pass
    print(throttler.check(user_id="user_1", ts=1000.0))
    print(throttler.check(user_id="user_2", ts=2000.5))
    _ = my_data
