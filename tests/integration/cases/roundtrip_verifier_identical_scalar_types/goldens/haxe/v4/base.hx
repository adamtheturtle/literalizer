class Fixture_roundtrip_verifier_identical_scalar_types_Haxe {
    public static function main() {
        final my_data = ([
            "value" => ([true, false, 0, 1] : Array<Dynamic>),
        ] : Map<String, Dynamic>);
    }
}
