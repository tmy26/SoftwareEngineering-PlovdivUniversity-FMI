import pandas as pd

# Read routes.dat and airports.dat
routes_df = pd.read_csv('/Users/vasenceto/Downloads/routes.dat', header=None, names=["Airline", "AirlineID",
                                                                                     "SourceAirport", "SourceAirportID",
                                                                                     "DestinationAirport", "DestinationAirportID",
                                                                                     "Codeshare", "Stops", "Equipment"])
airports_df = pd.read_csv('/Users/vasenceto/Downloads/airports.dat', header=None, names=["AirportID", "Name",
                                                                                         "City", "Country", "IATA",
                                                                                         "ICAO", "Latitude", "Longitude",
                                                                                         "Altitude", "Timezone", "DST",
                                                                                         "TzDatabase", "Type", "Source"])


airports_df['AirportID'] = airports_df['AirportID'].astype(str)

source_without_N = routes_df[routes_df['DestinationAirportID'] != '\\N']

destination_without_N = source_without_N[source_without_N['SourceAirportID'] != '\\N']

source_without_invalid_id = (
    destination_without_N)[destination_without_N['SourceAirportID'].isin(airports_df['AirportID'])]

destination_without_invalid_id = (
    source_without_invalid_id)[source_without_invalid_id['DestinationAirportID'].isin(airports_df['AirportID'])]

valid_IATA_source = (destination_without_invalid_id)[destination_without_invalid_id['SourceAirport'].isin(airports_df['IATA'])]

valid_IATA_dest = (valid_IATA_source)[valid_IATA_source['DestinationAirport'].isin(airports_df['IATA'])]

valid_IATA_dest = valid_IATA_dest.rename(columns={
    "Airline": "Airline:STRING",
    "AirlineID": "AirlineID:INTEGER",
    "SourceAirport": "SourceAirport:STRING",
    "SourceAirportID": ":START_ID",
    "DestinationAirport": "DestinationAirport:STRING",
    "DestinationAirportID": ":END_ID",
    "Codeshare": "Codeshare:STRING",
    "Stops": "Stops:INTEGER",
    "Equipment": "Equipment:STRING"
})

airports_df = airports_df.rename(columns={
    "AirportID": ":ID",
    "Name": "Name:STRING",
    "City": "City:STRING",
    "Country": "Country:STRING",
    "IATA": "IATA:STRING",
    "ICAO": "ICAO:STRING",
    "Latitude": "Latitude:FLOAT",
    "Longitude": "Longitude:FLOAT",
    "Altitude": "Altitude:STRING",
    "Timezone": "Timezone:STRING",
    "DST": "DST:STRING",
    "TzDatabase": "TzDatabase:STRING",
    "Type": "Type:STRING",
    "Source": "Source:STRING"
})

valid_IATA_dest = valid_IATA_dest[[":START_ID", ":END_ID", "SourceAirport:STRING",
                                   "Airline:STRING", "DestinationAirport:STRING",
                                   "AirlineID:INTEGER", "Codeshare:STRING",
                                   "Stops:INTEGER", "Equipment:STRING"]]

valid_routes = valid_IATA_dest.copy()

# Save the valid routes to CSV
valid_routes.to_csv('/Users/vasenceto/Desktop/cleaned_routes.csv', index=False)
airports_df.to_csv('/Users/vasenceto/Desktop/cleaned_airports.csv', index=False)
