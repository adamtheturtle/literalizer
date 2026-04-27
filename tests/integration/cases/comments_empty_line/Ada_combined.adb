with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("a"),
        --
        AStr ("b")
    ];
begin
    my_data := AList'[
        AStr ("a"),
        --
        AStr ("b")
    ];
end Check;
