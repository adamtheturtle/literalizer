class Fixture_coercion_heterogeneous_array_toml_Haxe {
    public static function main() {
        final my_data = ([
            "_" => ([1, 2.5, 3] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
