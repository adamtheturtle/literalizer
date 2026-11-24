class Fixture_literalize_ref_mutable_nested_Haxe_ref {
    public static function main() {
        var shared = ([
            1,
            2,
        ] : Array<Dynamic>);
        var second = ([
            3,
            4,
        ] : Array<Dynamic>);
        var my_data = ([
            shared,
            second,
        ] : Array<Dynamic>);
    }
}
