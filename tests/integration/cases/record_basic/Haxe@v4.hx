class Fixture_record_basic_Haxe {
    public static function main() {
        final my_data = ([
            "id" => 1,
            "label" => "She said \"hello\", then waved",
            "enabled" => false,
            "related_ids" => ([1, 2, 3] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
