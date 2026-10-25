class Fixture_nested_mixed_types_Haxe_combined {
    public static function main() {
        var my_data = ([
            ([1, 2] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            ([1, 2] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
