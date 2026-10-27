class Fixture_nested_sequence_with_empty_sibling_Haxe {
    public static function main() {
        final my_data = ([
            ([([1] : Array<Dynamic>)] : Array<Dynamic>),
            ([([] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
