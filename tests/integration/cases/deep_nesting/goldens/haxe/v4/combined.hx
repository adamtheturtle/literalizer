class Fixture_deep_nesting_Haxe_combined {
    public static function main() {
        var my_data = ([
            "level1" => (["level2" => (["level3" => (["level4" => (["value" => "deep", "items" => (["a", "b"] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>), "sibling" => 42] : Map<String, Dynamic>), "tags" => ([(["name" => "tag1", "meta" => (["priority" => 1, "labels" => (["x", "y"] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
        my_data = ([
            "level1" => (["level2" => (["level3" => (["level4" => (["value" => "deep", "items" => (["a", "b"] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>), "sibling" => 42] : Map<String, Dynamic>), "tags" => ([(["name" => "tag1", "meta" => (["priority" => 1, "labels" => (["x", "y"] : Array<Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
