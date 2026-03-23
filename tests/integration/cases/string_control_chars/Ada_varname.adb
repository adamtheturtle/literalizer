procedure Check is
   my_data : A_Val := AList'(
       AStr ("line1\r\nline2"),
       AStr ("line1\rline2"),
       AStr ("")
   );
begin
   null;
end Check;
