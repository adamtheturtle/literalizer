class Fixture_call_dotted_empty_result_binding_Haxe_type_hints_safe_call {
    public static function main() {
        var thing = { go: function(value:Dynamic):Dynamic return null };
        final my_data = thing.go(([] : Array<Dynamic>));
    }
}
