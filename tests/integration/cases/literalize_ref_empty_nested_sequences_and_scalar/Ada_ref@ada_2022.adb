with A_Stub; use A_Stub;
procedure Main is
    seed : A_Val := AInt (1);
    my_data : A_Val := AList'[
        AList'[],
        AList'[AList'[]],
        seed
    ];
begin
    null;
end Main;
