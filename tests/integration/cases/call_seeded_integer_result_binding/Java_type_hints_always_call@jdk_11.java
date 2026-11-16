class Main {
private static int eventIndex;
private static void observeEvent(int actual) {
    final int[] expected = {2, 42, 1, 42, 2, 142};
    if (eventIndex >= 6 || actual != expected[eventIndex]) throw new AssertionError("receiver event changed");
    eventIndex++;
}
static int make_widget(int count) { observeEvent(1); observeEvent(count); return count + 100; }
static void consume(int count) { observeEvent(2); observeEvent(count); }
static void verify_events() { if (eventIndex != 6) throw new AssertionError("missing receiver events"); }
    public static void main() {
int my_data = 42;
consume(my_data);
my_data = make_widget(42);
consume(my_data);
verify_events();
    }
}
