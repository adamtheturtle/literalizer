class Fixture_nested_array_maps_Haxe {
    public static function main() {
        final my_data = ([
            "groups" => ([([(["id" => 1] : Map<String, Dynamic>)] : Array<Dynamic>), ([(["id" => 2] : Map<String, Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
