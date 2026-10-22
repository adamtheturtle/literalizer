with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AInt (1), AStr ("value")], AList'[AInt (1), AInt (2)], AList'[]],
        AList'[AList'[], AList'[], AList'[AInt (3), AInt (4)]]
    ];
begin
    null;
end Main;
