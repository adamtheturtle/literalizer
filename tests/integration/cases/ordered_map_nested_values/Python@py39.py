from collections import OrderedDict
my_data = {
    "ordered": OrderedDict([
        # ordered entry
        ("name", "Alice"),
        ("scores", {
            # score meaning
            1: "first",
            2: "second",  # latest score
        }),
    ]),
}
