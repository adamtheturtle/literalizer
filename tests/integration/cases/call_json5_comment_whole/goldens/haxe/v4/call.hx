class Fixture_call_json5_comment_whole_Haxe_call {
    public static function main() {
        var expectedEvents:Array<Int> = [1, 42];
        var eventIndex:Int = 0;
        function observeEvent(actual:Int):Void {
            if (eventIndex >= 2 || actual != expectedEvents[eventIndex]) throw "receiver event changed";
            eventIndex++;
        }
        function f(a:Int):Int { observeEvent(1); observeEvent(a); return a + 100; }
        function verify_events():Void { if (eventIndex != 2) throw "missing receiver events"; }
        // scalar heading
        // second heading line
        // scalar inline
        // inline continuation
        // scalar trailing
        f(42);
        verify_events();
    }
}
