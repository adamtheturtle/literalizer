class Fixture_call_per_element_false_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 1];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 2 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function process(data:Int):Int { observeEvent(1); observeEvent(data); return data + 100; }
        function verify_events():Void { if (eventIndex != 2) throw "missing receiver events"; }
        process(1);
        verify_events();
    }
}
