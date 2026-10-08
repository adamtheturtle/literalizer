class Fixture_raku_single_element_containers_Haxe {
    public static function main() {
        final my_data = ([
            "single_map" => ([([] : Map<String, Dynamic>)] : Array<Dynamic>),
            "single_list" => ([([1] : Array<Dynamic>)] : Array<Dynamic>),
            "single_deep" => ([([([2] : Array<Dynamic>)] : Array<Dynamic>)] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
