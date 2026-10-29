class Fixture_call_process_member_Haxe_call {
    public static function main() {
        var app = { process: { fetch: function(data:Dynamic):Dynamic return null } };
        app.process.fetch((["data" => "hello"] : Map<String, Dynamic>));
        app.process.fetch((["data" => 42] : Map<String, Dynamic>));
        app.process.fetch((["data" => true] : Map<String, Dynamic>));
    }
}
