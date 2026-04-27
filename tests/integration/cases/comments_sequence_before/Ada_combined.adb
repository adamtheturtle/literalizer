with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        -- first
        AStr ("a"),
        -- second
        AStr ("b")
    ];
begin
    my_data := AList'[
        -- first
        AStr ("a"),
        -- second
        AStr ("b")
    ];
end Check;
