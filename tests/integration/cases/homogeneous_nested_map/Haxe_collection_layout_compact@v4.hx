class Fixture_homogeneous_nested_map_Haxe_collection_layout_compact {
    public static function main() {
        final my_data = ([
            "first" => (["x" => 1, "y" => 2] : Map<String, Dynamic>),
            "second" => (["z" => 3] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
