class Fixture_call_wrapper_alternate_name_collision_Haxe_call {
    public static function main() {
        function check_wrapper(a:Dynamic):Dynamic return null;
        check_wrapper(42);
    }
}
