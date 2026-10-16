class Fixture_call_nim_dotted_empty_result_binding_Haxe_call {
    public static function main() {
        var thing = { go: function(value:Dynamic):Dynamic return null };
        final my_data = thing.go(([] : Array<Dynamic>));
    }
}
