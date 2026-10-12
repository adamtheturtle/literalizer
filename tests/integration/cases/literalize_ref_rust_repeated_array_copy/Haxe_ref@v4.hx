class Fixture_literalize_ref_rust_repeated_array_copy_Haxe_ref {
    public static function main() {
        final shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            shared,
            shared,
        ] : Array<Dynamic>);
    }
}
