Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"description", "# not a comment" & Chr(10)},
        {"name", "foo"}
    }
End Module
