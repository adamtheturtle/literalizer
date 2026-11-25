class Fixture_jsonc_escaped_quote_slashes_Haxe {
    public static function main() {
        final my_data = ([
            "text" => "a\"//b",
        ] : Map<String, Dynamic>);
    }
}
