class Fixture_cpp_mixed_sibling_maps_Haxe {
    public static function main() {
        final my_data = ([
            ([(["a" => 1] : Map<String, Dynamic>), (["a" => null] : Map<String, Dynamic>), 42] : Array<Dynamic>),
            ([(["a" => 1] : Map<String, Dynamic>), (["a" => "s"] : Map<String, Dynamic>), 42] : Array<Dynamic>),
            ([(["a" => 1] : Map<String, Dynamic>), (["a" => null] : Map<String, Dynamic>)] : Array<Dynamic>),
            ([(["a" => 1] : Map<String, Dynamic>), (["a" => "s"] : Map<String, Dynamic>)] : Array<Dynamic>),
        ] : Array<Dynamic>);
    }
}
