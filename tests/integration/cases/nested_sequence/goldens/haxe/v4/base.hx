class Fixture_nested_sequence_Haxe {
    public static function main() {
        final my_data = ([
            true,
            "hi",
            ([1, 2] : Array<Dynamic>),
            null,
        ] : Array<Dynamic>);
    }
}
