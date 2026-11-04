class Fixture_call_dotted_nonempty_result_binding_Haxe_type_hints_always_call {
    public static function main() {
        var thing = { go: function(value:Dynamic):Dynamic return null };
        final my_data:Array<Dynamic> = thing.go(([1] : Array<Dynamic>));
    }
}
