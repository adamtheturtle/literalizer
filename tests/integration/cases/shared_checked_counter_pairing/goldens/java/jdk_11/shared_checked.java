
class Main {
    static int checks = 0;
    static class Counter {
        int calls = 0;
        boolean accept(String user, double timestamp) {
            if (!user.equals(calls == 0 ? "user_1" : "user_2") || timestamp != 100.0 + calls) throw new AssertionError("receiver arguments changed");
            calls++;
            return user.equals("user_1");
        }
    }
    static void checkResult(boolean actual, Object[] expected) {
        if (actual != (Boolean) expected[0] || !expected[1].equals(checks == 0 ? "first" : "second")) throw new AssertionError("paired result changed");
        checks++;
    }
    public static void main() {
        Counter counter = new Counter();
        checkResult(counter.accept("user_1", 100.0), new Object[]{true, "first"});
        checkResult(counter.accept("user_2", 101.0), new Object[]{false, "second"});
        if (counter.calls != 2 || checks != 2) throw new AssertionError("calls skipped");
    }
}
