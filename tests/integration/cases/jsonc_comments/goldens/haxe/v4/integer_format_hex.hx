class Fixture_jsonc_comments_Haxe_integer_format_hex {
    public static function main() {
        final my_data = ([
            // A JSONC input case with both comment forms.
            "url" => "https://example.org/a/*b*/",  // detail
            // continued
            "count" => 0x2,  // trailing line comment
        ] : Map<String, Dynamic>);
    }
}
