class Fixture_cpp14_widened_sibling_maps_Haxe {
    public static function main() {
        final my_data = ([
            "a" => (["k" => 1] : Map<String, Dynamic>),
            "b" => (["k" => "s"] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
