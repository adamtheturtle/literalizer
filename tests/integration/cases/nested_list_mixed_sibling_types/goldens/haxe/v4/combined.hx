class Fixture_nested_list_mixed_sibling_types_Haxe_combined {
    public static function main() {
        var my_data = ([
            ([1, 2] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            ([1, 2] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
