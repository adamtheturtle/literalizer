class Fixture_json5_comment_lexemes_Haxe_combined {
    public static function main() {
        var my_data = ([
            // heading
            "a" => "single ' // data",
            "b" => "linecontinuation",
            "c" => "\\",  // actual comment
            "d" => "          ",  // final comment
        ] : Map<String, Dynamic>);
        my_data = ([
            // heading
            "a" => "single ' // data",
            "b" => "linecontinuation",
            "c" => "\\",  // actual comment
            "d" => "          ",  // final comment
        ] : Map<String, Dynamic>);
    }
}
