Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"name", "Alice"},
        {"tags", New HashSet(Of Object) From {
            True,
            42,
            "apple"
        }}
    }
End Module
