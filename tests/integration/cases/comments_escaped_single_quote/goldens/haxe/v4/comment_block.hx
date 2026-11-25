class Fixture_comments_escaped_single_quote_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "key" => "it's here",  /* a comment */
        ] : Map<String, Dynamic>);
    }
}
