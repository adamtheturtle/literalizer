class Fixture_typescript_homogeneous_nested_map_Haxe {
    public static function main() {
        final my_data = ([
            "first" => (["x" => 1, "y" => 2] : Map<String, Dynamic>),
            "second" => (["z" => 3] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
