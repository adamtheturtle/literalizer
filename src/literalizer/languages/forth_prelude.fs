\ Default visitor bindings for literalizer's Forth backend (issue #2744).
\
\ The Forth backend literalizes a JSON document to a colon definition
\ that executes a sequence of small "constructor" words:
\
\   +obj / -obj    object start / end
\   +arr / -arr    array start / end
\   +key           ( c-addr u -- )      a member name
\   +int           ( n -- )             an integer value
\   +float         ( F: r -- )          a floating-point value
\   +str           ( c-addr u -- )      a string value
\   +bool          ( flag -- )          a boolean value
\   +null          ( -- )               a null value
\
\ These words are deliberately a thin, rebindable protocol: the same
\ literalized definition drives whichever visitor the caller binds.
\ This file ships the default binding -- a Forth Foundation Library
\ (FFL) `jos` JSON-output-stream writer that accumulates JSON into a
\ shared `json-out` stream -- so a literalized `: myData ... ;` is a
\ runnable JSON-producing program out of the box.  A caller who wants
\ to build a Forth-side data structure, walk into custom storage, emit
\ YAML, or compute over the values instead simply redefines any of the
\ words below before executing the definition; nothing here is special
\ to JSON beyond these bindings.
\
\ `include ffl/jos.fs` resolves through gforth's source-search path, so
\ the FFL checkout must be on that path (e.g. via `fpath+` or
\ `GFORTHPATH`) before this file is loaded.

include ffl/jos.fs

\ The shared JSON-output stream the default bindings write to.  Read it
\ back with `json-out str-get type` after executing the definition.
jos-create json-out

: +obj   ( -- )          json-out jos-write-start-object ;
: -obj   ( -- )          json-out jos-write-end-object ;
: +arr   ( -- )          json-out jos-write-start-array ;
: -arr   ( -- )          json-out jos-write-end-array ;
: +key   ( c-addr u -- ) json-out jos-write-name ;
: +int   ( n -- )        json-out jos-write-number ;
: +float ( F: r -- )     json-out jos-write-float ;
: +str   ( c-addr u -- ) json-out jos-write-string ;
: +bool  ( flag -- )     json-out jos-write-boolean ;
: +null  ( -- )          json-out jos-write-nil ;
