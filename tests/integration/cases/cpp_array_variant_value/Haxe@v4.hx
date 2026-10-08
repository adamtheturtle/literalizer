class Fixture_cpp_array_variant_value_Haxe {
    public static function main() {
        final my_data = ([
            "a" => 1,
            "b" => "x",
            "e" => ([1, 2] : Array<Dynamic>),
            "f" => (["g" => "h"] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
