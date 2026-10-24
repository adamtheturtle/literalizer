class Fixture_literalize_ref_pre_indented_Haxe_ref {
    public static function main() {
            final shared = ([
                1,
                2,
            ] : Array<Dynamic>);
            final my_data = ([
                "a" => shared,
            ] : Map<String, Dynamic>);
    }
}
