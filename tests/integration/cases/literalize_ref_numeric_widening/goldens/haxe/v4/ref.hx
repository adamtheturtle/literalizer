class Fixture_literalize_ref_numeric_widening_Haxe_ref {
    public static function main() {
        final floatingValue = 1.5;
        final integerValue = 2.0;
        final my_data = ([
            floatingValue,
            integerValue,
        ] : Array<Dynamic>);
    }
}
