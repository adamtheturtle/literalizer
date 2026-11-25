class Fixture_literalize_ref_sibling_map_Haxe_ref {
    public static function main() {
        final siblingMap = ([
            "k" => 2,
        ] : Map<String, Dynamic>);
        final my_data = ([
            (["k" => 1] : Map<String, Dynamic>),
            siblingMap,
        ] : Array<Dynamic>);
    }
}
