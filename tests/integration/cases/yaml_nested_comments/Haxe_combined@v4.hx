class Fixture_yaml_nested_comments_Haxe_combined {
    public static function main() {
        var my_data = ([
            "a" => ([
                // inner note
                "b" => 1,  // inline b
            ] : Map<String, Dynamic>),
            "list" => ([
                1,  // first
                2,  // second
            ] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
        my_data = ([
            "a" => ([
                // inner note
                "b" => 1,  // inline b
            ] : Map<String, Dynamic>),
            "list" => ([
                1,  // first
                2,  // second
            ] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
