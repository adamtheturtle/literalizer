class Fixture_record_named_nested_record_Haxe {
    public static function main() {
        final my_data = ([
            "project" => "alpha",
            "lead_task" => (["id" => 100, "description" => "first task", "is_done" => false, "blocks" => ([102, 103] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
