with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AInt (0),
        AList'[AList'[AStr ("plain")]]
    ];
begin
    null;
end Main;
