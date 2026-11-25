class Fixture_call_wrapper_zip_integer_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 1, 2, 101, 3, 42];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function process(value:Int):Int { observeEvent(1); observeEvent(value); return value + 100; }
        function emit(actual:Int, zipped:Int):Void { observeEvent(2); observeEvent(actual); observeEvent(3); observeEvent(zipped); }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        emit(process(1), 42);
        verify_events();
    }
}
