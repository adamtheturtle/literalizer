using System;
class Counter {
    public int calls;
    public bool accept(string user, double timestamp) {
        if (user != (calls == 0 ? "user_1" : "user_2") || timestamp != 100.0 + calls) throw new System.Exception("receiver arguments changed");
        calls++;
        return user == "user_1";
    }
}
class Program {
    static int checks;
    static void checkResult(bool actual, (bool, string) expected) {
        if (actual != expected.Item1 || expected.Item2 != (checks == 0 ? "first" : "second")) throw new System.Exception("paired result changed");
        checks++;
    }
    static void Main() {
        var counter = new Counter();
        checkResult(counter.accept("user_1", 100.0), (true, "first"));
        if (counter.calls != 1 || checks != 1) throw new System.Exception("calls skipped");
    }
}
