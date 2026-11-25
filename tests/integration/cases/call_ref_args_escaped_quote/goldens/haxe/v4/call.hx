class Fixture_call_ref_args_escaped_quote_Haxe_call {
    public static function main() {
        function process(v:Dynamic):Dynamic return null;
        final my_str = "a\"b";
        process(my_str);
    }
}
