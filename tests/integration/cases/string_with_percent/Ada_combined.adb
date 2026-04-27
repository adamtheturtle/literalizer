with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AStr ("100% done"),
        AStr ("%(name) is here")
    ];
begin
    my_data := AList'[
        AStr ("100% done"),
        AStr ("%(name) is here")
    ];
end Check;
