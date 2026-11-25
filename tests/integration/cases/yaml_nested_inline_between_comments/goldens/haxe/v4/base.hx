class Fixture_yaml_nested_inline_between_comments_Haxe {
    public static function main() {
        final my_data = ([
            ([2, "hello"] : Array<Dynamic>),  // trailing note
            // next element
            ([3, "world"] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
