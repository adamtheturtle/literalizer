class Fixture_comments_empty_line_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "a",
            /* */
            "b",
        ] : Array<Dynamic>);
    }
}
