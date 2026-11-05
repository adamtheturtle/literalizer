class Fixture_roundtrip_verifier_object_order_and_numeric_equivalence_Haxe {
    public static function main() {
        final my_data = ([
            "b" => null,
            "a" => (["y" => ([1.0] : Array<Dynamic>), "x" => false] : Map<String, Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
