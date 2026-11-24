class Fixture_literalize_ref_array_mixed_bound_values_Haxe_ref {
    public static function main() {
        final arrayValue = ([
            1,
            2,
        ] : Array<Dynamic>);
        final scalarValue = 3;
        final my_data = ([
            arrayValue,
            scalarValue,
        ] : Array<Dynamic>);
    }
}
