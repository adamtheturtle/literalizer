with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        -- strings stay data
        AStr ("https://example.org/a/*b*/"),  -- URL annotation
        AStr ("escaped quote: "" // still data"),
        AStr ("backslash: \"),  -- outside the string
        AStr ("/* not a comment */")
    ];
begin
    my_data := AList'[
        -- strings stay data
        AStr ("https://example.org/a/*b*/"),  -- URL annotation
        AStr ("escaped quote: "" // still data"),
        AStr ("backslash: \"),  -- outside the string
        AStr ("/* not a comment */")
    ];
end Main;
