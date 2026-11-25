using System;
class Check {
static int eventIndex;
static void ObserveEvent(int actual) {
    int[] expected = {1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42};
    if (eventIndex >= 12 || actual != expected[eventIndex]) throw new System.Exception("receiver event changed");
    eventIndex++;
}
static int process(int value) { ObserveEvent(1); ObserveEvent(value); return value + 100; }
static void emit(int actual, int zipped) { ObserveEvent(2); ObserveEvent(actual); ObserveEvent(3); ObserveEvent(zipped); }
static void verify_events() { if (eventIndex != 12) throw new System.Exception("missing receiver events"); }
    public static void Main() {
emit(process(1), 41);
emit(process(2), 42);
verify_events();
    }
}
