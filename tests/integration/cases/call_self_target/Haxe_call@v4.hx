class Fixture_call_self_target_Haxe_call {
    public static function main() {
        function self(value:Dynamic):Dynamic return null;
        self("hello");
    }
}
