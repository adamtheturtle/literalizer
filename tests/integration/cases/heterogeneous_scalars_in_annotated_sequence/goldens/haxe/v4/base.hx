class Fixture_heterogeneous_scalars_in_annotated_sequence_Haxe {
    public static function main() {
        final my_data = ([
            true,
            1.5,
            null,
            "2020-01-01",
            "2020-01-01T00:00:00+00:00",
            ([] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
