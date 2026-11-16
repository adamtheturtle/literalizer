class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {1, 1};
    if (eventIndex >= 2 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int process(int value) { observeEvent(1); observeEvent(value); return value + 100; }
static void verify_events() { if (eventIndex != 2) throw new AssertionError("missing receiver events"); }
    public static void main() {
process(1);
verify_events();
    }
}
