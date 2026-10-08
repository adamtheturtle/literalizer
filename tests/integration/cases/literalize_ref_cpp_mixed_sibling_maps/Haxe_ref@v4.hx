class Fixture_literalize_ref_cpp_mixed_sibling_maps_Haxe_ref {
    public static function main() {
        final actual = 42;
        final my_data = ([
            (["$ref" => 1] : Map<String, Dynamic>),
            (["$ref" => null] : Map<String, Dynamic>),
            actual,
        ] : Array<Dynamic>);
    }
}
