Reject declaration modifiers that cannot be combined. Java and C# accept one
visibility modifier except for ``private protected``, and a C# ``const`` field
cannot also be declared ``static`` or ``readonly``.
Emitting every modifier produced source such as ``public private int x``, which
does not compile.
