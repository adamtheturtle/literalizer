class Fixture_coercion_homogeneous_dict_toml_Haxe {
    public static function main() {
        final my_data = ([
            "_" => (["a" => 1, "b" => 2] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
