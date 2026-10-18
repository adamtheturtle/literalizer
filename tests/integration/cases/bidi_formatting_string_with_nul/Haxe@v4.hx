class Fixture_bidi_formatting_string_with_nul_Haxe {
    public static function main() {
        final my_data = ([
            "v" => "a‪\x00é😀b",
        ] : Map<String, Dynamic>);
    }
}
