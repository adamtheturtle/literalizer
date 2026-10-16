class Fixture_literalize_ref_cpp_external_empty_Haxe_ref_default {
    public static function main() {
        final item = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        (void)my_data;
        my_data = item;
        (void)my_data;
    }
}
