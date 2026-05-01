Imports System.Collections.Generic
Module Check
    Dim my_var = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim item_var = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim my_data = New Dictionary(Of String, Object) From {
        {"key", my_var},
        {"items", New Object() {item_var, New Dictionary(Of String, Object) From {{"fallback", "value"}}}}
    }
End Module
