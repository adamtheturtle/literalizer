class Fixture_call_process_root_Haxe_call {
    public static function main() {
        var process = { api: { fetch: function(data:Dynamic):Dynamic return null } };
        process.api.fetch((["data" => "hello"] : Map<String, Dynamic>));
        process.api.fetch((["data" => 42] : Map<String, Dynamic>));
        process.api.fetch((["data" => true] : Map<String, Dynamic>));
    }
}
