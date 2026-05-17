class Fixture_doubly_nested_list_with_empty_sibling_Haxe {
    public static function main() {
        final my_data = ([
            ([([1, 2] : Array<Dynamic>)] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            ([([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
