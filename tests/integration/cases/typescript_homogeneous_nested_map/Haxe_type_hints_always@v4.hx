class Fixture_typescript_homogeneous_nested_map_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "first" => (["x" => 1, "y" => 2] : Map<String, Dynamic>),
            "second" => (["z" => 3] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
