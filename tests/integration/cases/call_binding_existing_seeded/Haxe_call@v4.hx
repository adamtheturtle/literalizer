class Fixture_call_binding_existing_seeded_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 42, 1, 42, 1, 142];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function make_widget(count:Int):Int { observeEvent(1); observeEvent(count); return count + 100; }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        var my_data = 42;
        make_widget(my_data);
        my_data = make_widget(my_data);
        make_widget(my_data);
        verify_events();
    }
}
