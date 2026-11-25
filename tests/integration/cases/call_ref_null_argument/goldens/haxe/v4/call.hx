class Fixture_call_ref_null_argument_Haxe_call {
    public static function main() {
        function consume(value:Dynamic):Dynamic return null;
        final value = null;
        consume(value);
    }
}
