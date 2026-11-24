class Fixture_yaml_anchor_marks_in_comment_Haxe_type_hints_always {
    public static function main() {
        final my_data:Dynamic = // An anchor and an alias marker, written only inside this comment: &a *a
        null;
    }
}
