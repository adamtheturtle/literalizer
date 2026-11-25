using System;
class Check {
static int eventIndex;
static void ObserveEvent(int actual) {
    int[] expected = {2, 42, 1, 42, 2, 142};
    if (eventIndex >= 6 || actual != expected[eventIndex]) throw new System.Exception("receiver event changed");
    eventIndex++;
}
static int make_widget(int count) { ObserveEvent(1); ObserveEvent(count); return count + 100; }
static void consume_widget(int count) { ObserveEvent(2); ObserveEvent(count); }
static void verify_events() { if (eventIndex != 6) throw new System.Exception("missing receiver events"); }
    public static void Main() {
var my_data = 42;
consume_widget(my_data);
my_data = make_widget(my_data); // note
consume_widget(my_data);
verify_events();
    }
}
