class Fixture_literalize_ref_repeated_empty_array_Haxe_ref {
    public static function main() {
        final shared = ([] : Array<Dynamic>);
        final my_data = ([
            shared,
            shared,
        ] : Array<Dynamic>);
    }
}
