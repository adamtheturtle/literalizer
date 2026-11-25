class Fixture_nested_list_mixed_sibling_types_Haxe {
    public static function main() {
        final my_data = ([
            ([1, 2] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            (["a", "b"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
