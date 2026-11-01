// Query Programmes2025 (Import)
let
    Source = Excel.Workbook(File.Contents(DataFolder & "Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    Programmes2025_Sheet = Source{[Item="Programmes2025",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Programmes2025_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"utility", type text}, {"winter_peak_mw", Int64.Type}, {"summer_peak_mw", Int64.Type}, {"smart_meter_share", type number}, {"time_varying_rate_share_pct", type number}, {"demand_response_potential_mw", type number}, {"losses_pct", type number}})
in
    #"Changed Type"
