using System;
class Check {
static int eventIndex;
static void ObserveEvent(int actual) {
    int[] expected = {1, 1};
    if (eventIndex >= 2 || actual != expected[eventIndex]) throw new System.Exception("receiver event changed");
    eventIndex++;
}
static int process(int value) { ObserveEvent(1); ObserveEvent(value); return value + 100; }
static void verify_events() { if (eventIndex != 2) throw new System.Exception("missing receiver events"); }
    public static void Main() {
var value = 1;
process(value);
verify_events();
    }
}
