class Fixture_literalize_ref_cpp_external_assignment_Haxe_ref_default {
    public static function main() {
        final ref_data = ([
            1,
            2,
        ] : Array<Dynamic>);
        final my_data = ([
            0,
        ] : Array<Dynamic>);
        (void)my_data;
        my_data = ref_data;
        (void)my_data;
    }
}
