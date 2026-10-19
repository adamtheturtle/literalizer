with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AInt (1), AList'[AInt (2)]],
        AList'[AInt (3), AList'[AInt (4)]]
    ];
begin
    null;
end Main;
