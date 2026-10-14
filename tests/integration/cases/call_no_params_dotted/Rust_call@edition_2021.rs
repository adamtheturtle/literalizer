fn main() {
    struct ThrottlerType;
    impl ThrottlerType { fn check(&self) {} }
    let throttler = ThrottlerType;
    throttler.check();
    throttler.check();
}
