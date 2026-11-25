class Main {
static class ThrottlerType_ { Object check(Object arg0, Object arg1) { return null; } }
static ThrottlerType_ throttler = new ThrottlerType_();
static Object emit(Object arg0) { return null; }
    public static void main() {
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
    }
}
