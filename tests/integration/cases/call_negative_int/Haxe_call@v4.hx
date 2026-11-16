class Fixture_call_negative_int_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, -1, 1, -2, 1, -3];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function process(value:Int):Int { observeEvent(1); observeEvent(value); return value + 100; }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        process(-1);
        process(-2);
        process(-3);
        verify_events();
    }
}
