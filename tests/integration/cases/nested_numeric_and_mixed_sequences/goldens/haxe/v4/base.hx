class Fixture_nested_numeric_and_mixed_sequences_Haxe {
    public static function main() {
        final my_data = ([
            "numbers" => ([1, 2] : Array<Dynamic>),
            "nested" => (["inner" => ([3] : Array<Dynamic>)] : Map<String, Dynamic>),
            "mixed" => ([4, "five"] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
