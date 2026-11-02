// Query COUNTY_OUTAGE_MAP (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "county_outage_map.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"COUNTY_FIPS", "COUNTY_LABEL", "DOMINION_ONLY_COUNTY", "CUSTOMERS_BASIS", "MAP_FLAG", "READINGS_2015_24", "MINUTES_NON_MED_AVG_2015_24", "EVENTS_PER_10K_AVG_2015_24", "EVENTS_PER_10K_2015_19", "EVENTS_PER_10K_2020_24", "STORM_DAYS_AVG_2015_24"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"COUNTY_FIPS", type text}, {"COUNTY_LABEL", type text}, {"DOMINION_ONLY_COUNTY", type logical}, {"CUSTOMERS_BASIS", Int64.Type}, {"MAP_FLAG", type text}, {"READINGS_2015_24", type number}, {"MINUTES_NON_MED_AVG_2015_24", type number}, {"EVENTS_PER_10K_AVG_2015_24", type number}, {"EVENTS_PER_10K_2015_19", type number}, {"EVENTS_PER_10K_2020_24", type number}, {"STORM_DAYS_AVG_2015_24", type number}}, "en-US")
in
    Typed
