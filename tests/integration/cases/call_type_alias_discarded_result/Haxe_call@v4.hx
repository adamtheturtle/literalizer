class Fixture_call_type_alias_discarded_result_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 1];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 2 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function process(value:Int):Int { observeEvent(1); observeEvent(value); return value + 100; }
        function verify_events():Void { if (eventIndex != 2) throw "missing receiver events"; }
        process(1);
        verify_events();
    }
}
