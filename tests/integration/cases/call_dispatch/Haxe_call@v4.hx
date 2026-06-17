class Fixture_call_dispatch_Haxe_call {
    public static function main() {
        function store_item(key:Dynamic, value:Dynamic):Dynamic return null;
        function read_item(key:Dynamic):Dynamic return null;
        store_item(1, 10);
        read_item(1);
    }
}
