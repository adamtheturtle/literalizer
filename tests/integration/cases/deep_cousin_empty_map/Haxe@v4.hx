class Fixture_deep_cousin_empty_map_Haxe {
    public static function main() {
        final my_data = ([
            (["outer" => (["inner" => (["x" => 1] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>),
            (["outer" => (["inner" => ([] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
