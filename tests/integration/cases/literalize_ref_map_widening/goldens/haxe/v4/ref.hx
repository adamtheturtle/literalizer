class Fixture_literalize_ref_map_widening_Haxe_ref {
    public static function main() {
        final stringMap = ([
            "k" => "s",
        ] : Map<String, Dynamic>);
        final my_data = ([
            stringMap,
            (["k" => 1] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
