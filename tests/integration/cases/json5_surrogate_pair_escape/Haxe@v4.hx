class Fixture_json5_surrogate_pair_escape_Haxe {
    public static function main() {
        final my_data = ([
            "astral" => "😀",
            "mixed" => "a😀b",
            "count" => 2,
            "list" => (["😀", 1] : Array<Dynamic>),
            "nested" => (["inner" => "😀"] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
