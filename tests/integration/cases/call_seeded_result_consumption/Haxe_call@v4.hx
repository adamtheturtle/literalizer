class Fixture_call_seeded_result_consumption_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [2, 0, 1, 1, 2, 101];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 6 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function make_widget(count:Int):Int { observeEvent(1); observeEvent(count); return count + 100; }
        function consume_widget(count:Int):Void { observeEvent(2); observeEvent(count); }
        function verify_events():Void { if (eventIndex != 6) throw "missing receiver events"; }
        var my_data = 0;
        consume_widget(my_data);
        my_data = make_widget(1);
        consume_widget(my_data);
        verify_events();
    }
}
