fn main() {
    struct ThrottlerType_;
    impl ThrottlerType_ { fn check<>(&self, ) {} }
    let throttler = ThrottlerType_;
    throttler.check();
    throttler.check();
}
