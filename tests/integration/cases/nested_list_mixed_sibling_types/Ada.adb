with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AList'[AInt (1), AInt (2)],
        AList'[],
        AList'[AStr ("a"), AStr ("b")]
    ];
begin
    null;
end Check;
