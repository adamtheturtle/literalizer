class Fixture_dict_with_nulls_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            "name" => "Alice",
            "score" => null,
            "age" => 0x1e,
        ] : Map<String, Dynamic>);
    }
}
