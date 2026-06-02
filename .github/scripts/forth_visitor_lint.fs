\ Lint-only visitor bindings for the Forth backend's structured output
\ (issue #2744).
\
\ The `Lint Forth` step in `.github/workflows/lint.yml` loads this file
\ before each generated `*.fth` fixture so that the visitor words
\ (`+obj`/`-obj`/`+arr`/`-arr`/`+key`/`+int`/`+float`/`+str`/`+bool`/
\ `+null`) resolve.  The bindings here are deliberately minimal: each
\ consumes exactly its operands (matching the stack effects documented
\ in `src/literalizer/languages/forth_prelude.fs`) and does nothing
\ else.
\
\ This validates the same thing the old flat-stack fixtures did -- the
\ generated code parses and every word it names is defined -- without
\ the single-document-root state constraint of the shipped FFL `jos`
\ default binding.  Most fixtures are colon *definitions* that gforth
\ only compiles (never executes) at load time; the call fixtures
\ execute top-level statements, and a value fragment such as a bare
\ `42 +int` is not a complete JSON document, so the document-oriented
\ `jos` writer would reject it.  The real `jos` binding in
\ `forth_prelude.fs` is exercised end-to-end on a full document by
\ `run_forth_roundtrip.py` instead.

: +obj   ( -- )          ;
: -obj   ( -- )          ;
: +arr   ( -- )          ;
: -arr   ( -- )          ;
: +key   ( c-addr u -- ) 2drop ;
: +int   ( n -- )        drop ;
: +float ( F: r -- )     fdrop ;
: +str   ( c-addr u -- ) 2drop ;
: +bool  ( flag -- )     drop ;
: +null  ( -- )          ;
