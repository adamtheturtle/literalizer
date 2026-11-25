class Fixture_dict_all_null_trailing_comment_Haxe {
    public static function main() {
        final my_data = ([
            "a" => null,
            "b" => null,
            // trailing
        ] : Map<String, Dynamic>);
    }
}
