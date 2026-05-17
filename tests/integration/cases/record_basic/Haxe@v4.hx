class Fixture_record_basic_Haxe {
    public static function main() {
        final my_data = ([
            "id" => 1,
            "description" => "She said \"hello\", then waved",
            "is_done" => false,
            "blocks" => ([1, 2, 3] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
