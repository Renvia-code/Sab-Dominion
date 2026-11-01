// Query Programmes2025 (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "programmes_2025.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Selected = Table.SelectColumns(Promoted, {"utility", "winter_peak_mw", "summer_peak_mw", "smart_meter_share", "time_varying_rate_share_pct", "demand_response_potential_mw", "losses_pct"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"utility", type text}, {"winter_peak_mw", Int64.Type}, {"summer_peak_mw", Int64.Type}, {"smart_meter_share", type number}, {"time_varying_rate_share_pct", type number}, {"demand_response_potential_mw", type number}, {"losses_pct", type number}}, "en-US")
in
    Typed
