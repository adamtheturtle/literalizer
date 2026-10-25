class Fixture_nested_maps_with_opposed_value_types_Haxe {
    public static function main() {
        final my_data = ([
            (["input" => (["name" => "alice", "city" => "paris"] : Map<String, Dynamic>), "expected" => (["count" => 1, "total" => 2] : Map<String, Dynamic>)] : Map<String, Dynamic>),
            (["input" => (["name" => 10, "city" => 20] : Map<String, Dynamic>), "expected" => (["count" => "done", "total" => "pending"] : Map<String, Dynamic>)] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
