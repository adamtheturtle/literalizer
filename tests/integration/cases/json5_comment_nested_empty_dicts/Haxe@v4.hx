class Fixture_json5_comment_nested_empty_dicts_Haxe {
    public static function main() {
        final my_data = ([
            // outer heading
            // first empty
            "a" => ([] : Map<String, Dynamic>),
            // second empty
            "b" => ([] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
