class Fixture_call_dotted_transform_stub_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        var tracer = { emit: function(_arg:Dynamic):Dynamic return null };
        tracer.emit(process("hello"));
        tracer.emit(process(42));
        tracer.emit(process(true));
    }
}
