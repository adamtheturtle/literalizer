class Fixture_nested_sequences_Haxe {
    public static function main() {
        final my_data = ([
            ([([1, 2] : Array<Dynamic>), ([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
            ([([5] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
