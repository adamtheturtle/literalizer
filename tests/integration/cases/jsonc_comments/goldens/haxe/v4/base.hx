class Fixture_jsonc_comments_Haxe {
    public static function main() {
        final my_data = ([
            // A JSONC input case with both comment forms.
            "url" => "https://example.org/a/*b*/",  // detail
            // continued
            "count" => 2,  // trailing line comment
        ] : Map<String, Dynamic>);
    }
}
