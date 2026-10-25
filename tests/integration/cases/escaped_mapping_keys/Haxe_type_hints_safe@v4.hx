class Fixture_escaped_mapping_keys_Haxe_type_hints_safe {
    public static function main() {
        final my_data = ([
            "quote\"backslash\\" => 1,
            "line\nbreak" => 2,
            "$(literal)${text}" => 3,
            "RStr prefix" => 4,
        ] : Map<String, Dynamic>);
    }
}
