deep = {
    {
        "one",
        "two"
    },
    {
        "three",
        "four"
    }
};
my_data = struct(
    'a', struct(
        'b', struct(
            'c', deep
        )
    )
);
