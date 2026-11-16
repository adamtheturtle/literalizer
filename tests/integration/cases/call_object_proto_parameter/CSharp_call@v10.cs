using System;
class Check {
static int eventIndex;
static void ObserveEvent(int actual) {
    int[] expected = {1, 1};
    if (eventIndex >= 2 || actual != expected[eventIndex]) throw new System.Exception("receiver event changed");
    eventIndex++;
}
static int capture(int __proto__) { ObserveEvent(1); ObserveEvent(__proto__); return __proto__ + 100; }
static void verify_events() { if (eventIndex != 2) throw new System.Exception("missing receiver events"); }
    public static void Main() {
capture(1);
verify_events();
    }
}
