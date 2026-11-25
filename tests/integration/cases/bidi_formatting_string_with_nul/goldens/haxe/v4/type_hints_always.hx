class Fixture_bidi_formatting_string_with_nul_Haxe_type_hints_always {
    public static function main() {
        final my_data:Map<String, Dynamic> = ([
            "v" => "a‪\x00é😀b",
        ] : Map<String, Dynamic>);
    }
}
