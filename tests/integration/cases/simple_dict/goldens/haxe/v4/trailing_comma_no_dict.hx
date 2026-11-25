class Fixture_simple_dict_Haxe_trailing_comma_no_dict {
    public static function main() {
        final my_data = ([
            "name" => "Alice",
            "age" => 30,
            "active" => true,
            "score" => null
        ] : Map<String, Dynamic>);
    }
}
