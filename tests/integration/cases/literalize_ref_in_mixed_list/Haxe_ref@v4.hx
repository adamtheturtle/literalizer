class Fixture_literalize_ref_in_mixed_list_Haxe_ref {
    public static function main() {
        final refX = ([
            "_" => "_",
        ] : Map<String, Dynamic>);
        final my_data = ([
            refX,
            1,
            2,
        ] : Array<Dynamic>);
    }
}
