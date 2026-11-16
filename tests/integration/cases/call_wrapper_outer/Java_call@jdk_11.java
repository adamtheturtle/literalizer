class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {1, 42, 2, 142};
    if (eventIndex >= 4 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int process(int value) { observeEvent(1); observeEvent(value); return value + 100; }
static void emit(int value) { observeEvent(2); observeEvent(value); }
static void verify_events() { if (eventIndex != 4) throw new AssertionError("missing receiver events"); }
    public static void main() {
emit(process(42));
verify_events();
    }
}
