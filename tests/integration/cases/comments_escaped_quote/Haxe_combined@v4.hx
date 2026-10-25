class Fixture_comments_escaped_quote_Haxe_combined {
    public static function main() {
        var my_data = ([
            "key" => "value \" # not a comment",  // real
        ] : Map<String, Dynamic>);
        my_data = ([
            "key" => "value \" # not a comment",  // real
        ] : Map<String, Dynamic>);
    }
}
