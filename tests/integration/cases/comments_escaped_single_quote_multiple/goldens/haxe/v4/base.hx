class Fixture_comments_escaped_single_quote_multiple_Haxe {
    public static function main() {
        final my_data = ([
            "host" => "it's here",  // a comment
            "port" => 80,  // another
        ] : Map<String, Dynamic>);
    }
}
