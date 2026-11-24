class Fixture_call_ref_external_known_null_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final item = null;
        consume(item);
    }
}
