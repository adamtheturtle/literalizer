class Fixture_string_control_chars_Haxe {
    public static function main() {
        final my_data = ([
            "line1\r\nline2",
            "line1\rline2",
            "",
        ] : Array<Dynamic>);
    }
}
