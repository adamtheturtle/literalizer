class Fixture_jsonc_comment_nulls_Haxe {
    public static function main() {
        final my_data = ([
            // null heading
            // before null
            "a" => null,  // first null
            "b" => null,  // second null
        ] : Map<String, Dynamic>);
    }
}
