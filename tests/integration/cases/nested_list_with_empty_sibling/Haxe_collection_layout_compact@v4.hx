class Fixture_nested_list_with_empty_sibling_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            ([1, 2] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            ([3, 4] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
