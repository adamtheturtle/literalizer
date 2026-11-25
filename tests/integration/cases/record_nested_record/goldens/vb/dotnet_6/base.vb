Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"id", 1},
        {"owner", New Dictionary(Of String, Object) From {{"name", "Alice"}, {"age", 30}}}
    }
End Module
