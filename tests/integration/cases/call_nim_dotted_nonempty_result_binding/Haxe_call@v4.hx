class Fixture_call_nim_dotted_nonempty_result_binding_Haxe_call {
    public static function main() {
        var thing = { go: function(value:Dynamic):Dynamic return null };
        final my_data = thing.go(([1] : Array<Dynamic>));
    }
}
