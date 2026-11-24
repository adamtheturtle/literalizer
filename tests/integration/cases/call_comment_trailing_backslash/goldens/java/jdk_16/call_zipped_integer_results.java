class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42};
    if (eventIndex >= 12 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int process(int value) { observeEvent(1); observeEvent(value); return value + 100; }
static void emit(int actual, int zipped) { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped); }
static void verify_events() { if (eventIndex != 12) throw new AssertionError("missing receiver events"); }
    public static void main() {
emit(process(1), 41);
emit(process(2), 42);
verify_events();
    }
}
