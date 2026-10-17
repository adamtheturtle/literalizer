with A_Stub; use A_Stub;
procedure Main is
    existing : A_Val := AInt (1);
    my_data : A_Val := AList'[
        AInt (0),
        AList'[AList'[existing]]
    ];
begin
    null;
end Main;
