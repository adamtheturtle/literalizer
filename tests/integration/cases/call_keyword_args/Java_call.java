    static class _throttlerType { Object check(Object... a) { return null; } }
    static _throttlerType throttler = new _throttlerType();
    static Object print(Object... a) { return null; }
class Check {
    public static void check() {
print(throttler.check("user_1", 1000.0));
print(throttler.check("user_2", 2000.5));
    }
}
