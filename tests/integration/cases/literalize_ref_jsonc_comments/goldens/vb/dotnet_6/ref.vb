Imports System.Collections.Generic
Module Check
    Dim Existing = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    ' This reference names an existing variable.
    ' reference target
    Dim my_data = Existing
End Module
