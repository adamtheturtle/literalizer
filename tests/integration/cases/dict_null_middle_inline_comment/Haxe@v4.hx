class Fixture_dict_null_middle_inline_comment_Haxe {
    public static function main() {
        final my_data = ([
            "host" => "localhost",
            "port" => null,  // not configured yet
            "debug" => true,
        ] : Map<String, Dynamic>);
    }
}
