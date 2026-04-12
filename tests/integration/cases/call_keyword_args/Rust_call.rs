fn main() {
    struct _ThrottlerType;
    impl _ThrottlerType { fn check<T, U>(&self, _: T, _: U) {} }
    let throttler = _ThrottlerType;
    fn print<T>(_: T) {}
    print(throttler.check("user_1", 1000.0))
    print(throttler.check("user_2", 2000.5))
    let _ = my_data;
}
