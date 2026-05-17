class Fixture_call_comments_dict_args_Haxe_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        // Test cases
        process((["type" => "create", "pr_id" => "pr_1"] : Map<String, Dynamic>));  // first case
        process((["type" => "update", "pr_id" => "pr_2"] : Map<String, Dynamic>));  // second case
        // third case
        process((["type" => "delete", "pr_id" => "pr_3"] : Map<String, Dynamic>));
    }
}
