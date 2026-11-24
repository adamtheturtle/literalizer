class Fixture_mixed_nested_collection_types_Haxe {
    public static function main() {
        final my_data = ([
            "lists" => ([([1] : Array<Dynamic>), (["x"] : Array<Dynamic>), ([] : Array<Dynamic>)] : Array<Dynamic>),
            "maps" => ([(["x" => 1] : Map<String, Dynamic>), (["x" => "s"] : Map<String, Dynamic>)] : Array<Dynamic>),
            "empties" => (["a" => ([1] : Array<Dynamic>), "b" => ([] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
