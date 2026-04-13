fn main() {
    struct ThrottlerType_;
    impl ThrottlerType_ { fn check<A, B>(&self, _user_id: A, _ts: B) {} }
    let throttler = ThrottlerType_;
    fn emit<A>(__arg: A) {}
    emit(throttler.check("user_1", 1000.0));
    emit(throttler.check("user_2", 2000.5));
}
