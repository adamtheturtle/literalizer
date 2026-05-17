class Fixture_call_mixed_type_dicts_Haxe_call {
    public static function main() {
        var app = { mgr: { run: function(operation:Dynamic):Dynamic return null } };
        app.mgr.run((["type" => "create", "pr_id" => "pr_1", "draft" => true] : Map<String, Dynamic>));
        app.mgr.run((["type" => "create", "pr_id" => "pr_2"] : Map<String, Dynamic>));
    }
}
