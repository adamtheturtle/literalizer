class Fixture_literalize_ref_repeated_array_scalars_Haxe_ref {
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
