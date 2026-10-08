class Fixture_literalize_ref_nonstring_names_Haxe_ref {
    public static function main() {
        final actual = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            (["$ref" => 1] : Map<String, Dynamic>),
            (["$ref" => null] : Map<String, Dynamic>),
            actual,
        ] : Array<Dynamic>);
    }
}
