class Fixture_literalize_ref_repeated_nested_collection_Haxe_ref {
    public static function main() {
        final shared = ([
            ([1, 2] : Array<Dynamic>),
            (["value" => 1] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
        final my_data = ([
            shared,
            shared,
        ] : Array<Dynamic>);
    }
}
