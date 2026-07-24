class Fixture_record_named_nested_record_Haxe {
    public static function main() {
        final my_data = ([
            "project" => "alpha",
            "lead_item" => (["id" => 100, "label" => "first item", "enabled" => false, "related_ids" => ([102, 103] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
