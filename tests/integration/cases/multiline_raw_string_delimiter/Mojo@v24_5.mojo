def main():
    var my_data: List[String] = List([
        "custom base after empty collision: )\"\nvalue",
        "custom suffix after base collision: )\" and )x0\"\nvalue",
        "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
        "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue",
    ])
    _ = my_data
