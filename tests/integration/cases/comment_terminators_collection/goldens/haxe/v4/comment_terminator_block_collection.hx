class Fixture_comment_terminators_collection_Haxe_comment_terminator_block_collection {
    public static function main() {
        final my_data = ([
            /* before first: * / |# -} *) (* ) =# ]] %} ]# % #> */
            "first",  /* inline first: * / |# -} *) (* ) =# ]] %} ]# % #> */
            /* before second: * / |# -} *) (* ) =# ]] %} ]# % #> */
            "second",
            /* trailing: * / |# -} *) (* ) =# ]] %} ]# % #> */
        ] : Array<Dynamic>);
    }
}
