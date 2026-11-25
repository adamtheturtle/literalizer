with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AInt (1), AInt (2)],
        AList'[],
        AList'[AInt (3), AInt (4)]
    ];
begin
    my_data := AList'[
        AList'[AInt (1), AInt (2)],
        AList'[],
        AList'[AInt (3), AInt (4)]
    ];
end Main;
