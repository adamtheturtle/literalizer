with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("a     b     c"),
        AStr ("a" & Character'Val(13) & "     b")
    ];
begin
    null;
end Main;
