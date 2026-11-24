Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"outer", New Dictionary(Of String, Object) From {{"a", 1}, {"b", "x"}, {"c", Nothing}}}
    }
End Module
