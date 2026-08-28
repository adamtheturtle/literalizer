class Fixture_yaml_unread_comment_slots_Haxe {
    public static function main() {
        final my_data = ([
            "flow" => ([
                1,
                // After the first element.
                2,
            ] : Array<Dynamic>),
            // Between the key and its value.
            "gap" => 3,
            // On the block scalar header.
            "block" => "Text.\n",
            "anchored" => 4,
            "alias" => 4,
            // On the alias.
        ] : Map<String, Dynamic>);
    }
}
