class Fixture_inline_comment_trailing_backslash_Haxe {
    public static function main() {
        final my_data = ([
            "a" => 1,  // inline ending backslash \ .
            "b" => 2,
        ] : Map<String, Dynamic>);
    }
}
