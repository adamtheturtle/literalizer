class Fixture_call_ref_v_null_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final value = null;
        consume(value);
    }
}
