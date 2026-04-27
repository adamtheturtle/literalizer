with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("foo"),
        AStr ("bar"),
        AStr ("baz")
    ];
begin
    my_data := AList'[
        AStr ("foo"),
        AStr ("bar"),
        AStr ("baz")
    ];
end Check;
