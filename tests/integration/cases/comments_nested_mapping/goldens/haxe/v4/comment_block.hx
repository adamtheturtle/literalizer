class Fixture_comments_nested_mapping_Haxe_comment_block {
    public static function main() {
        final my_data = ([
            "a" => ([
                /* indented */
                "x" => 1,
            ] : Map<String, Dynamic>),
            "b" => 2,
        ] : Map<String, Dynamic>);
    }
}
