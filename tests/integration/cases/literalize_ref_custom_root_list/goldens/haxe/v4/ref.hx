class Fixture_literalize_ref_custom_root_list_Haxe_ref {
    public static function main() {
        var whole = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = whole;
        my_data = whole;
    }
}
