with A_Stub; use A_Stub;
procedure Main is
    shared : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    my_data : A_Val := shared;
end Main;
