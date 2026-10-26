class Fixture_literalize_ref_empty_nested_sequences_and_scalar_Haxe_ref {
    public static function main() {
        final seed = 1;
        final my_data = ([
            ([] : Array<Dynamic>),
            ([([] : Array<Dynamic>)] : Array<Dynamic>),
            seed,
        ] : Array<Dynamic>);
    }
}
