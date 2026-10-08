class Fixture_json5_raw_line_separators_Haxe {
    public static function main() {
        final my_data = ([
            "double" => "a         b",
            "single" => "c         d",
            "both" => "e         f         g",
            "continued" => "hi",
            "escaped backslash" => "j\\         k",
        ] : Map<String, Dynamic>);
    }
}
