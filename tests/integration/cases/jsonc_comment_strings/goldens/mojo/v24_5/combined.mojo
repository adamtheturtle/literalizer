def main():
    var my_data: List[String] = List([
        # strings stay data
        "https://example.org/a/*b*/",  # URL annotation
        "escaped quote: \" // still data",
        "backslash: \\",  # outside the string
        "/* not a comment */",
    ])
    _ = my_data
    my_data = List([
        # strings stay data
        "https://example.org/a/*b*/",  # URL annotation
        "escaped quote: \" // still data",
        "backslash: \\",  # outside the string
        "/* not a comment */",
    ])
    _ = my_data
