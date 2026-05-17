class Fixture_nested_mixed_dict_Haxe {
    public static function main() {
        final my_data = ([
            "outer" => (["a" => 1, "b" => "x", "c" => null] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
