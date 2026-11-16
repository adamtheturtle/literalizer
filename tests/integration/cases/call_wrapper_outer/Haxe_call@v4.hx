class Fixture_call_wrapper_outer_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 42, 2, 142];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 4 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function process(value:Int):Int { observeEvent(1); observeEvent(value); return value + 100; }
        function emit(value:Int):Void { observeEvent(2); observeEvent(value); }
        function verify_events():Void { if (eventIndex != 4) throw "missing receiver events"; }
        emit(process(42));
        verify_events();
    }
}
