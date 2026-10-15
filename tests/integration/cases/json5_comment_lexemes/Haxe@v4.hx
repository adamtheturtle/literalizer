class Fixture_json5_comment_lexemes_Haxe {
    public static function main() {
        final my_data = ([
            // heading
            "a" => "single ' // data",
            "b" => "linecontinuation",
            "c" => "\\",  // actual comment
            "d" => "          ",  // final comment
        ] : Map<String, Dynamic>);
    }
}
