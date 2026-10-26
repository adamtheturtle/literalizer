class Fixture_call_wrapper_outer_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        function emit(_arg:Dynamic):Dynamic return null;
        emit(process(42));
    }
}
