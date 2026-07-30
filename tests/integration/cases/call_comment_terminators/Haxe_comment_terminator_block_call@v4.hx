class Fixture_call_comment_terminators_Haxe_comment_terminator_block_call {
    public static function main() {
        function process(value:Dynamic):Dynamic return null;
        process("Dune");  /* first: * / |# -} *) ) =# ]] %} ]# % #> */
        process("Solaris");
        process("Neuromancer");  /* third: * / |# -} *) ) =# ]] %} ]# % #> */
    }
}
