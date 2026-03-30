procedure Check is
   my_data : A_Val := AList'(
       AStr ("C:\path\to\file"),
       AStr ("back\\slash"),
       AStr ("hello \""world\"""),
       AStr ("path\to ""# file")
   );
begin
   null;
end Check;
