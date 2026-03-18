"""Built-in language specifications for common programming languages."""

from __future__ import annotations

from .ada import Ada
from .bash import Bash
from .c import C
from .clojure import Clojure
from .cpp import Cpp
from .crystal import Crystal
from .csharp import CSharp
from .d import D
from .dart import Dart
from .elixir import Elixir
from .erlang import Erlang
from .fsharp import FSharp
from .go import Go
from .groovy import Groovy
from .haskell import Haskell
from .java import Java
from .javascript import JavaScript
from .julia import Julia
from .kotlin import Kotlin
from .lua import Lua
from .matlab import Matlab
from .nim import Nim
from .ocaml import OCaml
from .occam import Occam
from .perl import Perl
from .php import Php
from .powershell import PowerShell
from .python import Python
from .r import R
from .ruby import Ruby
from .rust import Rust
from .scala import Scala
from .swift import Swift
from .typescript import TypeScript
from .zig import Zig

# Backward-compatible default instances.
ADA = Ada()
BASH = Bash()
CLOJURE = Clojure()
CPP = Cpp()
CRYSTAL = Crystal()
CSHARP = CSharp()
DART = Dart()
ELIXIR = Elixir()
ERLANG = Erlang()
FSHARP = FSharp()
GO = Go()
GROOVY = Groovy()
HASKELL = Haskell()
JAVA = Java()
JAVASCRIPT = JavaScript()
JULIA = Julia()
KOTLIN = Kotlin()
LUA = Lua()
MATLAB = Matlab()
NIM = Nim()
OCAML = OCaml()
OCCAM = Occam()
PERL = Perl()
PHP = Php()
POWERSHELL = PowerShell()
PYTHON = Python()
RUBY = Ruby()
RUST = Rust()
SCALA = Scala()
SWIFT = Swift()
TYPESCRIPT = TypeScript()
ZIG = Zig()

__all__ = [
    "ADA",
    "BASH",
    "CLOJURE",
    "CPP",
    "CRYSTAL",
    "CSHARP",
    "DART",
    "ELIXIR",
    "ERLANG",
    "FSHARP",
    "GO",
    "GROOVY",
    "HASKELL",
    "JAVA",
    "JAVASCRIPT",
    "JULIA",
    "KOTLIN",
    "LUA",
    "MATLAB",
    "NIM",
    "OCAML",
    "OCCAM",
    "PERL",
    "PHP",
    "POWERSHELL",
    "PYTHON",
    "RUBY",
    "RUST",
    "SCALA",
    "SWIFT",
    "TYPESCRIPT",
    "ZIG",
    "Ada",
    "Bash",
    "C",
    "CSharp",
    "Clojure",
    "Cpp",
    "Crystal",
    "D",
    "Dart",
    "Elixir",
    "Erlang",
    "FSharp",
    "Go",
    "Groovy",
    "Haskell",
    "Java",
    "JavaScript",
    "Julia",
    "Kotlin",
    "Lua",
    "Matlab",
    "Nim",
    "OCaml",
    "Occam",
    "Perl",
    "Php",
    "PowerShell",
    "Python",
    "R",
    "Ruby",
    "Rust",
    "Scala",
    "Swift",
    "TypeScript",
    "Zig",
]
