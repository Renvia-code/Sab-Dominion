// Query OUTAGE_EVENTS_TOP10 (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "outage_events_top10.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"RANK", "EVENT_KEY", "START_DAY", "PEAK_DAY", "STORM_TYPE", "TROPICAL_CYCLONE", "PEAK_CUSTOMERS_OUT", "PEAK_SUSTAINED_1H", "HOURS_ABOVE_10K", "CUSTOMER_HOURS", "HOURS_TO_50PCT", "HOURS_TO_90PCT", "HOURS_TO_99PCT", "DOE417_CUSTOMERS_MAX", "STARTS_ON_MED_PROXY_DAY"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"RANK", Int64.Type}, {"EVENT_KEY", type text}, {"START_DAY", type datetime}, {"PEAK_DAY", type datetime}, {"STORM_TYPE", type text}, {"TROPICAL_CYCLONE", type text}, {"PEAK_CUSTOMERS_OUT", type number}, {"PEAK_SUSTAINED_1H", type number}, {"HOURS_ABOVE_10K", type number}, {"CUSTOMER_HOURS", type number}, {"HOURS_TO_50PCT", type number}, {"HOURS_TO_90PCT", type number}, {"HOURS_TO_99PCT", type number}, {"DOE417_CUSTOMERS_MAX", type number}, {"STARTS_ON_MED_PROXY_DAY", type logical}}, "en-US")
in
    Typed
