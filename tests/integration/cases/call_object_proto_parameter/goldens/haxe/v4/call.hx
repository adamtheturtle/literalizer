class Fixture_call_object_proto_parameter_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 1];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 2 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function capture(__proto__:Int):Int { observeEvent(1); observeEvent(__proto__); return __proto__ + 100; }
        function verify_events():Void { if (eventIndex != 2) throw "missing receiver events"; }
        capture(1);
        verify_events();
    }
}
