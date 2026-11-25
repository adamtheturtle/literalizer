class Fixture_call_binding_existing_next_line_comment_Haxe_type_hints_always_call {
    public static function main() {
        var expectedEvents:Array<Int> = [2, 42, 1, 42, 2, 142];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function make_widget(count:Int):Int { observeEvent(1); observeEvent(count); return count + 100; }
        function consume_widget(count:Int):Void { observeEvent(2); observeEvent(count); }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        var my_data:Dynamic = 42;
        consume_widget(my_data);
        my_data = make_widget(42);
        // note
        consume_widget(my_data);
        verify_events();
    }
}
