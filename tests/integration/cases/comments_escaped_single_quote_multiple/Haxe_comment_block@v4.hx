class Fixture_comments_escaped_single_quote_multiple_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "host" => "it's here",  /* a comment */
            "port" => 80,  /* another */
        ] : Map<String, Dynamic>);
    }
}
