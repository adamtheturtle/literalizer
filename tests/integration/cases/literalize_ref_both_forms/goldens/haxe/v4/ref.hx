class Fixture_literalize_ref_both_forms_Haxe_ref {
    public static function main() {
        var sharedValues = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = ([
            "a" => sharedValues,
        ] : Map<String, Dynamic>);
        my_data = ([
            "a" => sharedValues,
        ] : Map<String, Dynamic>);
    }
}
