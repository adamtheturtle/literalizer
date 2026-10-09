class Fixture_literalize_ref_cpp_repeated_owned_Haxe_ref {
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
