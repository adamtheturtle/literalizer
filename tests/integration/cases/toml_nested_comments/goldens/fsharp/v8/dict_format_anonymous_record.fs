module Main

let my_data = {|
    dotted = {|
        first = 1L;
        second = 2L
    |};
    plain = 3L;
    entries = [
        {|
            name = "one"
        |};
        {|
            name = "two"
        |}
    ];
    table = {|
        inner = 4L
    |}
|}
