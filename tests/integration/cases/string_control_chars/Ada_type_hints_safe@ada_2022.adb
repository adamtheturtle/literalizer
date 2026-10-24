with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("line1" & Character'Val(13) & Character'Val(10) & "line2"),
        AStr ("line1" & Character'Val(13) & "line2"),
        AStr ("" & Character'Val(1))
    ];
begin
    null;
end Main;
