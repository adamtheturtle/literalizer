with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AList'[AInt (1), AStr ("a")],
        AList'[AInt (2), AStr ("b")]
    ];
begin
    null;
end Check;
