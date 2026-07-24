Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"project", "alpha"},
        {"lead_item", New Dictionary(Of String, Object) From {{"id", 100}, {"label", "first item"}, {"enabled", False}, {"related_ids", New Integer() {102, 103}}}}
    }
End Module
