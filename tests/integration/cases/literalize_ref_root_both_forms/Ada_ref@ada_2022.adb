with A_Stub; use A_Stub;
procedure Main is
    whole : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := whole;
begin
    my_data := whole;
end Main;
