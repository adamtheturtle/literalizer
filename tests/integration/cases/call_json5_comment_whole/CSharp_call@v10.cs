using System;
class Check {
static int eventIndex;
static void ObserveEvent(int actual) {
    int[] expected = {1, 42};
    if (eventIndex >= 2 || actual != expected[eventIndex]) throw new System.Exception("receiver event changed");
    eventIndex++;
}
static int f(int a) { ObserveEvent(1); ObserveEvent(a); return a + 100; }
static void verify_events() { if (eventIndex != 2) throw new System.Exception("missing receiver events"); }
    public static void Main() {
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(42);
verify_events();
    }
}
