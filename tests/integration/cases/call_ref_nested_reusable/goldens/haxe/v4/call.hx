class Fixture_call_ref_nested_reusable_Haxe_call {
    public static function main() {
        function process(data:Dynamic):Dynamic return null;
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        process(([item, item] : Array<Dynamic>));
    }
}
