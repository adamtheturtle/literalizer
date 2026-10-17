class Fixture_string_carriage_return_line_feed_Haxe {
    public static function main() {
        final my_data = ([
            "cr" => "a\rb",
            "crlf" => "a\r\nb",
            "lf" => "a\nb",
        ] : Map<String, Dynamic>);
    }
}
