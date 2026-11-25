class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {1, -1, 1, -2, 1, -3};
    if (eventIndex >= 6 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int process(int value) { observeEvent(1); observeEvent(value); return value + 100; }
static void verify_events() { if (eventIndex != 6) throw new AssertionError("missing receiver events"); }
    public static void main() {
process(-1);
process(-2);
process(-3);
verify_events();
    }
}
