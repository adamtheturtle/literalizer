class Fixture_yaml_sequence_between_comments_Haxe {
    public static function main() {
        final my_data = ([
            (["item" => "existing"] : Map<String, Dynamic>),
            // This comment describes the next item.
            (["item" => "next"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
