class Fixture_call_ref_multiline_openers_Haxe_call {
    public static function main() {
        function consume(items:Dynamic, mapping:Dynamic):Dynamic return null;
        final foo = 42;
        consume(([
            ([
                "other" => 1,
            ] : Map<String, Dynamic>),
            foo,
        ] : Array<Dynamic>), ([
            "left" => foo,
            "other" => 1,
        ] : Map<String, Dynamic>));
    }
}
