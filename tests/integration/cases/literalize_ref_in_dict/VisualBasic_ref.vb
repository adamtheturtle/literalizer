Imports System.Collections.Generic
Module Check
    Dim MyVar = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim my_data = New Dictionary(Of String, Object) From {
        {"key", MyVar}
    }
End Module
