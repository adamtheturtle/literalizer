class Fixture_nested_sequences_Haxe_combined {
    public static function main() {
        var my_data = ([
            ([([1, 2] : Array<Dynamic>), ([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
            ([([5] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            ([([1, 2] : Array<Dynamic>), ([3, 4] : Array<Dynamic>)] : Array<Dynamic>),
            ([([5] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
