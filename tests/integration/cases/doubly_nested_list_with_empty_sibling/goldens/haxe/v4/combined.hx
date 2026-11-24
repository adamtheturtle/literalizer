class Fixture_doubly_nested_list_with_empty_sibling_Haxe_combined {
    public static function main() {
        var my_data = ([
            ([([1, 2] : Array<Dynamic>)] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            ([([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            ([([1, 2] : Array<Dynamic>)] : Array<Dynamic>),
            ([] : Array<Dynamic>),
            ([([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
