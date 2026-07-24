class Fixture_call_zip_values_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        function emit(_call:Dynamic, _zip:Dynamic):Dynamic return null;
        emit(process("hello"), "one");
        emit(process(42), "zero");
    }
}
