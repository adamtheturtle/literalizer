class Fixture_dict_escaped_quote_key_Haxe {
    public static function main() {
        final my_data = ([
            "a\"b" => 1,
        ] : Map<String, Dynamic>);
    }
}
