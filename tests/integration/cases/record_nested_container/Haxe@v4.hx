class Fixture_record_nested_container_Haxe {
    public static function main() {
        final my_data = ([
            "title" => "report",
            "tags" => (["draft", "urgent", "review"] : Array<Dynamic>),
            "priority" => 2,
        ] : Map<String, Dynamic>);
    }
}
