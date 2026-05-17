class Fixture_comments_nested_mapping_Haxe {
    public static function main() {
        final my_data = ([
            "a" => (["x" => 1] : Map<String, Dynamic>),
            "b" => 2,
        ] : Map<String, Dynamic>);
    }
}
