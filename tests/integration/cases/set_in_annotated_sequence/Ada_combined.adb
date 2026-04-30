with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        ASet'[],
        ASet'[AInt (1), AInt (2)],
        AList'[]
    ];
begin
    my_data := AList'[
        ASet'[],
        ASet'[AInt (1), AInt (2)],
        AList'[]
    ];
end Main;
