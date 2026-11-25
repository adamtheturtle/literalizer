class Fixture_call_unknown_ref_top_level_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final unknown_value = ([
            1,
        ] : Array<Dynamic>);
        process(unknown_value);
    }
}
