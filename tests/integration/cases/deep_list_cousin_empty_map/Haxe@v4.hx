class Fixture_deep_list_cousin_empty_map_Haxe {
    public static function main() {
        final my_data = ([
            (["items" => ([(["inner" => (["x" => 1] : Map<String, Dynamic>)] : Map<String, Dynamic>), (["inner" => ([] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
            (["items" => ([(["inner" => (["x" => 2] : Map<String, Dynamic>)] : Map<String, Dynamic>), (["inner" => ([] : Map<String, Dynamic>)] : Map<String, Dynamic>)] : Array<Dynamic>)] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
