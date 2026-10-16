module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    -- strings stay data
    PStr "https://example.org/a/*b*/",  -- URL annotation
    PStr "escaped quote: \" // still data",
    PStr "backslash: \\",  -- outside the string
    PStr "/* not a comment */"
]
