class Main {
static class ThrottlerType_ { Object check(Object... args) { return null; } }
static ThrottlerType_ throttler = new ThrottlerType_();
static Object emit(Object... args) { return null; }
    public static void main() {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
    }
}
