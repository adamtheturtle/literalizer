class Fixture_positional_empty_map_rows_Haxe {
    public static function main() {
        final my_data = ([
            "first" => ([([1, "value"] : Array<Dynamic>), ([] : Array<Dynamic>)] : Array<Dynamic>),
            "second" => ([([] : Array<Dynamic>), ([2, "other"] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
