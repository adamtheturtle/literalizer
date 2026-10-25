class Fixture_comments_escaped_single_quote_multiple_Haxe_combined {
    public static function main() {
        var my_data = ([
            "host" => "it's here",  // a comment
            "port" => 80,  // another
        ] : Map<String, Dynamic>);
        my_data = ([
            "host" => "it's here",  // a comment
            "port" => 80,  // another
        ] : Map<String, Dynamic>);
    }
}
