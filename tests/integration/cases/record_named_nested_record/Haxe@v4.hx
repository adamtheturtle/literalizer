class Fixture_record_named_nested_record_Haxe {
    public static function main() {
        final my_data = ([
            "collection" => "alpha",
            "featured_entry" => (["id" => 100, "label" => "first entry", "enabled" => false, "related_ids" => ([102, 103] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
