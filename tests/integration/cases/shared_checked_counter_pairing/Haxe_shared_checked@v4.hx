
class Counter {
    public var calls: Int = 0;
    public function new() {}
    public function accept(user: String, timestamp: Float): Bool {
        if (user != (calls == 0 ? "user_1" : "user_2") || timestamp != 100.0 + calls) throw "receiver arguments changed";
        calls++;
        return user == "user_1";
    }
}
class Fixture_shared_checked_counter_pairing_Haxe_shared_checked {
    static var checks: Int = 0;
    static function checkResult(actual: Bool, expected: Array<Dynamic>): Void {
        if (actual != expected[0] || expected[1] != (checks == 0 ? "first" : "second")) throw "paired result changed";
        checks++;
    }
    public static function main(): Void {
        var counter = new Counter();
        checkResult(counter.accept("user_1", 100.0), ([true, "first"] : Array<Dynamic>));
        checkResult(counter.accept("user_2", 101.0), ([false, "second"] : Array<Dynamic>));
        if (counter.calls != 2 || checks != 2) throw "calls skipped";
    }
}
