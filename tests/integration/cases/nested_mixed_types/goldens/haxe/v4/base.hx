class Fixture_nested_mixed_types_Haxe {
    public static function main() {
        final my_data = ([
            ([1, 2] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
