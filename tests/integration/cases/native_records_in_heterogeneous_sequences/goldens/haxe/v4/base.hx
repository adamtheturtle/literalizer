class Fixture_native_records_in_heterogeneous_sequences_Haxe {
    public static function main() {
        final my_data = ([
            "h" => ([1, "a", ([2, "b"] : Array<Dynamic>), (["k" => ([true] : Array<Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
