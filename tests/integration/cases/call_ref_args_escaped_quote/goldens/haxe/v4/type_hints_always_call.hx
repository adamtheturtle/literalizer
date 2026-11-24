class Fixture_call_ref_args_escaped_quote_Haxe_type_hints_always_call {
    public static function main() {
        function process(v:Dynamic):Dynamic return null;
        final my_str:Dynamic = "a\"b";
        process(my_str);
    }
}
