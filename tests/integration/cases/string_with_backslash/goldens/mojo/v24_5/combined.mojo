def main():
    var my_data: List[String] = List([
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ])
    _ = my_data
    my_data = List([
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ])
    _ = my_data
