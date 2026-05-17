class Fixture_call_keyword_args_Haxe_call {
    public static function main() {
        var throttler = { check: function(user_id:Dynamic, ts:Dynamic):Dynamic return null };
        function emit(_arg:Dynamic):Dynamic return null;
        emit(throttler.check("user_1", 1000.0));
        emit(throttler.check("user_2", 2000.5));
    }
}
