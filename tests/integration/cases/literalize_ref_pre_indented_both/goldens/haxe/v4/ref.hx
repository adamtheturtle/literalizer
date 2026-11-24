class Fixture_literalize_ref_pre_indented_both_Haxe_ref {
    public static function main() {
                var shared = ([
                    1,
                    2,
                ] : Array<Dynamic>);
                var my_data = ([
                    "a" => shared,
                ] : Map<String, Dynamic>);
                my_data = ([
                    "a" => shared,
                ] : Map<String, Dynamic>);
    }
}
