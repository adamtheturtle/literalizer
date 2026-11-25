class Fixture_toml_table_string_punctuation_Haxe {
    public static function main() {
        final my_data = ([
            "comma_hash" => "a,#b",
            "comma_space_hash" => "trail, # comment",
            "escaped_quote" => "quote \" and , #",
            "next_line" => "x        y",
            "line_separator" => "x         y",
            "paragraph_separator" => "x         y",
        ] : Map<String, Dynamic>);
    }
}
