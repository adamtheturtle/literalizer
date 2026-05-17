class Fixture_comments_bang_in_double_quote_Haxe {
    public static function main() {
        final my_data = ([
            "key" => "\"bang!\"",  // real
        ] : Map<String, Dynamic>);
    }
}
