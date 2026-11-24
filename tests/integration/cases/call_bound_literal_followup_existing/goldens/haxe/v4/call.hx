class Fixture_call_bound_literal_followup_existing_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [2, 42, 1, 42, 2, 142];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function make_widget(value:Int):Int { observeEvent(1); observeEvent(value); return value + 100; }
        function consume(value:Int):Void { observeEvent(2); observeEvent(value); }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        var my_data = 42;
        consume(my_data);
        my_data = make_widget(42);
        consume(my_data);
        verify_events();
    }
}
