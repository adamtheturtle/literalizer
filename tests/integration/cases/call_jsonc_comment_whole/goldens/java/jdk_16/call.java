class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {1, 42};
    if (eventIndex >= 2 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int f(int a) { observeEvent(1); observeEvent(a); return a + 100; }
static void verify_events() { if (eventIndex != 2) throw new AssertionError("missing receiver events"); }
    public static void main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
verify_events();
    }
}
