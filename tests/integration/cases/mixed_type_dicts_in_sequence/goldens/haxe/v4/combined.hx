class Fixture_mixed_type_dicts_in_sequence_Haxe_combined {
    public static function main() {
        var my_data = ([
            (["type" => "create", "pr_id" => "pr_1", "draft" => true] : Map<String, Dynamic>),
            (["type" => "create", "pr_id" => "pr_2"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
        my_data = ([
            (["type" => "create", "pr_id" => "pr_1", "draft" => true] : Map<String, Dynamic>),
            (["type" => "create", "pr_id" => "pr_2"] : Map<String, Dynamic>),
        ] : Array<Dynamic>);
    }
}
