class Fixture_comments_escaped_quote_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "key" => "value \" # not a comment",  /* real */
        ] : Map<String, Dynamic>);
    }
}
