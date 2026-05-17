class Fixture_call_no_params_dotted_Haxe_call {
    public static function main() {
        var throttler = { check: function():Dynamic return null };
        throttler.check();
        throttler.check();
    }
}
