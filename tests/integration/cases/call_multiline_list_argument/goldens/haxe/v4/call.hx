class Fixture_call_multiline_list_argument_Haxe_call {
    public static function main() {
        function process(xs:Dynamic):Dynamic return null;
        process(([
            1,
            2,
        ] : Array<Dynamic>));
        process(([
            3,
        ] : Array<Dynamic>));
    }
}
