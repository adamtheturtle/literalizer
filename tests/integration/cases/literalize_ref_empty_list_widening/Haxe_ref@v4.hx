class Fixture_literalize_ref_empty_list_widening_Haxe_ref {
    public static function main() {
        final emptyValues = ([] : Array<Dynamic>);
        final integerValues = ([
            1,
        ] : Array<Dynamic>);
        final my_data = ([
            emptyValues,
            integerValues,
        ] : Array<Dynamic>);
    }
}
