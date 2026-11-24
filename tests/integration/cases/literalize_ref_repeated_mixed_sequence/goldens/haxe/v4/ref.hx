class Fixture_literalize_ref_repeated_mixed_sequence_Haxe_ref {
    public static function main() {
        final shared = ([
            1,
            "x",
        ] : Array<Dynamic>);
        final my_data = ([
            shared,
            shared,
        ] : Array<Dynamic>);
    }
}
