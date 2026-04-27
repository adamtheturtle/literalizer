with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AFloat (0.0),
        AFloat (1.0),
        AFloat (1500.0),
        AFloat (0.001)
    ];
begin
    my_data := AList'[
        AFloat (0.0),
        AFloat (1.0),
        AFloat (1500.0),
        AFloat (0.001)
    ];
end Check;
