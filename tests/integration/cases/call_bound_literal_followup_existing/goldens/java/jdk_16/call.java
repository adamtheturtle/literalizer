class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {2, 42, 1, 42, 2, 142};
    if (eventIndex >= 6 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int make_widget(int value) { observeEvent(1); observeEvent(value); return value + 100; }
static void consume(int value) { observeEvent(2); observeEvent(value); }
static void verify_events() { if (eventIndex != 6) throw new AssertionError("missing receiver events"); }
    public static void main() {
var my_data = 42;
consume(my_data);
my_data = make_widget(42);
consume(my_data);
verify_events();
    }
}
