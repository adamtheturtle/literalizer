class Fixture_comments_nested_mapping_Haxe_combined {
    public static function main() {
        var my_data = ([
            "a" => ([
                // indented
                "x" => 1,
            ] : Map<String, Dynamic>),
            "b" => 2,
        ] : Map<String, Dynamic>);
        my_data = ([
            "a" => ([
                // indented
                "x" => 1,
            ] : Map<String, Dynamic>),
            "b" => 2,
        ] : Map<String, Dynamic>);
    }
}
