class Fixture_dict_null_leading_comment_Haxe {
    public static function main() {
        final my_data = ([
            // comment
            "name" => "Alice",
            "score" => null,
        ] : Map<String, Dynamic>);
    }
}
