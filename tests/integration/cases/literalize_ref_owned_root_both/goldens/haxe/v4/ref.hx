class Fixture_literalize_ref_owned_root_both_Haxe_ref {
    public static function main() {
        var shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = shared;
        my_data = shared;
    }
}
