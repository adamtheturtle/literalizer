class Fixture_literalize_ref_heterogeneous_list_Haxe_ref {
    public static function main() {
        final one = 1;
        final two = "s";
        final my_data = ([
            one,
            two,
        ] : Array<Dynamic>);
    }
}
