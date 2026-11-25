class Fixture_call_bound_scalar_declaration_variants_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final shared = 42;
        consume(shared);
    }
}
