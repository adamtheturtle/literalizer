class Fixture_yaml_sequence_between_comments_Haxe {
    public static function main() {
        final my_data = ([
            ([
                "item" => "existing",
                // This comment describes the next item.
            ] : Map<String, Dynamic>),
            (["item" => "next"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
