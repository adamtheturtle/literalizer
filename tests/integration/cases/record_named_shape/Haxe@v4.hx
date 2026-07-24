class Fixture_record_named_shape_Haxe {
    public static function main() {
        final my_data = ([
            (["id" => 100, "label" => "first item", "enabled" => false, "related_ids" => ([102, 103] : Array<Dynamic>)] : Map<String, Dynamic>),
            (["id" => 101, "label" => "second item", "enabled" => true, "related_ids" => ([100] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
