class Fixture_nested_sequence_declaration_modifiers_Haxe_type_hints_always {
    public static function main() {
        final my_data:Array<Dynamic> = ([
            ([] : Array<Dynamic>),
            ([1] : Array<Dynamic>),
            ([1, 2] : Array<Dynamic>),
            ([1, "x", true, null] : Array<Dynamic>),
            ([1, 2, 3, 4, 5, 6, 7, 8] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
