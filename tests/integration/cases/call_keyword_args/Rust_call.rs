fn main() {
    struct _ThrottlerType;
    impl _ThrottlerType { fn check(&self, _user_id: &dyn std::any::Any, _ts: &dyn std::any::Any) {} }
    let throttler = _ThrottlerType;
    fn print(_user_id: &dyn std::any::Any, _ts: &dyn std::any::Any) {}
    print(throttler.check("user_1", 1000.0));
    print(throttler.check("user_2", 2000.5));
    let _ = my_data;
}
