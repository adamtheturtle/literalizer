class Fixture_yaml_nested_comments_Haxe {
    public static function main() {
        final my_data = ([
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
