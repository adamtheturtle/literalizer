"""Built-in language specifications for common programming languages.

Each language class lives in its own module under this package
(e.g. ``literalizer.languages.python``) and is imported lazily.  Import
what you need directly::

    from literalizer.languages.python import Python

Use :func:`all_languages` to obtain the set of every built-in language
class — this triggers the import of every language module the first time
it is called.
"""

from literalizer._language import LanguageCls


def all_languages() -> frozenset[LanguageCls]:
    """Return the set of every built-in language specification class.

    Loads every language module on call.  Tests and tools that genuinely
    need the full set should call this once and reuse the result; for
    code that only needs a few languages, prefer importing them
    individually from their own modules.
    """
    # Local imports keep ``import literalizer.languages`` cheap.
    from .ada import Ada
    from .bash import Bash
    from .c import C
    from .clojure import Clojure
    from .cobol import Cobol
    from .common_lisp import CommonLisp
    from .cpp import Cpp
    from .crystal import Crystal
    from .csharp import CSharp
    from .d import D
    from .dart import Dart
    from .dhall import Dhall
    from .elixir import Elixir
    from .elm import Elm
    from .erlang import Erlang
    from .forth import Forth
    from .fortran import Fortran
    from .fsharp import FSharp
    from .gleam import Gleam
    from .go import Go
    from .groovy import Groovy
    from .haskell import Haskell
    from .hcl import Hcl
    from .java import Java
    from .javascript import JavaScript
    from .json5 import Json5
    from .jsonnet import Jsonnet
    from .julia import Julia
    from .kotlin import Kotlin
    from .lua import Lua
    from .matlab import Matlab
    from .mojo import Mojo
    from .nim import Nim
    from .nix import Nix
    from .norg import Norg
    from .objective_c import ObjectiveC
    from .ocaml import OCaml
    from .occam import Occam
    from .odin import Odin
    from .perl import Perl
    from .php import Php
    from .powershell import PowerShell
    from .purescript import PureScript
    from .python import Python
    from .r import R
    from .racket import Racket
    from .raku import Raku
    from .ruby import Ruby
    from .rust import Rust
    from .scala import Scala
    from .scheme import Scheme
    from .sml import Sml
    from .swift import Swift
    from .systemverilog import SystemVerilog
    from .tcl import Tcl
    from .toml import Toml
    from .typescript import TypeScript
    from .v import V
    from .vb import VisualBasic
    from .wren import Wren
    from .yaml import Yaml
    from .zig import Zig

    return frozenset(
        {
            Ada,
            Bash,
            C,
            Clojure,
            Cobol,
            CommonLisp,
            Cpp,
            Crystal,
            CSharp,
            D,
            Dart,
            Dhall,
            Elixir,
            Elm,
            Erlang,
            Forth,
            Fortran,
            FSharp,
            Gleam,
            Go,
            Groovy,
            Haskell,
            Hcl,
            Java,
            JavaScript,
            Json5,
            Jsonnet,
            Julia,
            Kotlin,
            Lua,
            Matlab,
            Mojo,
            Nim,
            Nix,
            Norg,
            ObjectiveC,
            OCaml,
            Occam,
            Odin,
            Perl,
            Php,
            PowerShell,
            PureScript,
            Python,
            R,
            Racket,
            Raku,
            Ruby,
            Rust,
            Scala,
            Scheme,
            Sml,
            Swift,
            SystemVerilog,
            Tcl,
            Toml,
            TypeScript,
            V,
            VisualBasic,
            Wren,
            Yaml,
            Zig,
        }
    )


__all__ = ["all_languages"]
