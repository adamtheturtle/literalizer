class Check {
    static class ThrottlerType_ { Object check(Object... a) { return null; } }
    static ThrottlerType_ throttler = new ThrottlerType_();
    static Object print(Object... a) { return null; }
    public static void check() {
print(throttler.check("user_1", 1000.0));
print(throttler.check("user_2", 2000.5));
    }
}
