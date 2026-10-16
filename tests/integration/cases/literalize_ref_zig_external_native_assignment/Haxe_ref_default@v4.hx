class Fixture_literalize_ref_zig_external_native_assignment_Haxe_ref_default {
    public static function main() {
        final shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        var my_data = ([
            0,
        ] : Array<Dynamic>);
        _ = &my_data;
        my_data = shared;
        _ = &my_data;
    }
}
