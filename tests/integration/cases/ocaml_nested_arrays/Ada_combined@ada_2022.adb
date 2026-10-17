with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AInt (1)]],
        AList'[AList'[]]
    ];
begin
    my_data := AList'[
        AList'[AList'[AInt (1)]],
        AList'[AList'[]]
    ];
end Main;
