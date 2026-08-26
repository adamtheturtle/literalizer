Reject declaration modifiers that cannot be combined. Java and C# accept one
visibility modifier, and a C# field is ``const`` or ``readonly`` but not both.
Emitting every modifier produced source such as ``public private int x``, which
does not compile.
