"""Built-in language specifications for common programming languages."""

from literalizer._language import LanguageCls

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
from .ruby import Ruby
from .rust import Rust
from .scala import Scala
from .scheme import Scheme
from .swift import Swift
from .systemverilog import SystemVerilog
from .toml import Toml
from .typescript import TypeScript
from .vb import VisualBasic
from .yaml import Yaml
from .zig import Zig

ALL_LANGUAGES: frozenset[LanguageCls] = frozenset(
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
        Ruby,
        Rust,
        Scala,
        Scheme,
        Swift,
        Toml,
        TypeScript,
        SystemVerilog,
        VisualBasic,
        Yaml,
        Zig,
    }
)

__all__ = [
    "ALL_LANGUAGES",
    "Ada",
    "Bash",
    "C",
    "CSharp",
    "Clojure",
    "Cobol",
    "CommonLisp",
    "Cpp",
    "Crystal",
    "D",
    "Dart",
    "Dhall",
    "Elixir",
    "Elm",
    "Erlang",
    "FSharp",
    "Fortran",
    "Gleam",
    "Go",
    "Groovy",
    "Haskell",
    "Hcl",
    "Java",
    "JavaScript",
    "Json5",
    "Jsonnet",
    "Julia",
    "Kotlin",
    "Lua",
    "Matlab",
    "Mojo",
    "Nim",
    "Norg",
    "OCaml",
    "ObjectiveC",
    "Occam",
    "Odin",
    "Perl",
    "Php",
    "PowerShell",
    "PureScript",
    "Python",
    "R",
    "Racket",
    "Ruby",
    "Rust",
    "Scala",
    "Scheme",
    "Swift",
    "SystemVerilog",
    "Toml",
    "TypeScript",
    "VisualBasic",
    "Yaml",
    "Zig",
]
