local thing = { go(before, populated, after):: null };
[
    thing.go(before=[], populated=[1], after=[]),
    thing.go(before=["text"], populated=[2], after=[]),
    thing.go(before=[], populated=["text"], after=[]),
    thing.go(before=["text"], populated=[2], after=[3]),
]
