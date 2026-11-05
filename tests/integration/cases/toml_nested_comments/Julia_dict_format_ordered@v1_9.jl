using DataStructures
my_data = OrderedDict(
    # About the first dotted key.
    # About the second dotted key.
    "dotted" => OrderedDict("first" => 1, "second" => 2),
    "plain" => 3,  # About the plain key.
    # Before the first entry.
    # Before the second entry.
    "entries" => [OrderedDict("name" => "one"), OrderedDict("name" => "two")],
    # Inside the table.
    "table" => OrderedDict("inner" => 4),
)
