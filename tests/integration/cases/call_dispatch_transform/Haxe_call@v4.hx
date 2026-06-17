class Fixture_call_dispatch_transform_Haxe_call {
    public static function main() {
        function record_value(value:Dynamic):Dynamic return null;
        function flush_buffer(count:Dynamic):Dynamic return null;
        function emit(_arg:Dynamic):Dynamic return null;
        emit(record_value(42));
        flush_buffer(3);
    }
}
