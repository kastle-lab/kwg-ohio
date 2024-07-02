import csv
import os
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
import pandas as pd

name_space = "http://kastle-lab.org/"
pfs = {
    "kl-res": Namespace(f"{name_space}lod/resource/"),
    "kl-ont": Namespace(f"{name_space}lod/ontology/"),
    "rdf": RDF,
    "rdfs": RDFS,
    "xsd": XSD,
    "owl": OWL,
    "time": TIME,
    "ssn": Namespace("http://www.w3.org/ns/ssn/"),
    "sosa": Namespace("http://www.w3.org/ns/sosa/"),
    "cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
}
g = Graph()
for prefix in pfs:
    g.bind(prefix, pfs[prefix])

# rdf:type shortcut
a = pfs["rdf"]["type"]

#defining entities
Marijuana = pfs["kl-ont"]["MarijuanaDispensary"]
SpatialObject = pfs["kl-ont"]["SpatialObject"]
Organization =  pfs["kl-ont"]["Organization"]
Person = pfs["kl-ont"]["Person"]
Location = pfs["kl-ont"]["Location"]
State = pfs["kl-ont"]["State"]
City = pfs["kl-ont"]["City"]
County = pfs["kl-ont"]["County"]

#defining object properties
hasLabel = pfs["rdfs"]["label"]
hasZip = pfs["kl-ont"]["hasZip"]
hasName = pfs["kl-ont"]["hasName"]
hasBusinessName = pfs["kl-ont"]["hasBusinessName"]
hasLicenseType = pfs["kl-ont"]["hasLicenseType"]
isLicenseStatus = pfs["kl-ont"]["isLicenseStatus"]
hasAddress = pfs["kl-ont"]["hasAddress"]
hasLicense = pfs["kl-ont"]["hasLicense"]
hasId = pfs["kl-ont"]["hasId"]
hasRepresentative = pfs["kl-ont"]["hasRepresentative"]
residesInState = pfs["kl-ont"]["residesInState"]
residesInCity = pfs["kl-ont"]["residesInCity"]
residesInCounty = pfs["kl-ont"]["residesInCounty"]

# Reading the restaurant data from csv file
# for a better experience, we can pass the file name through CLI arguments
with open('Ohio_Medical_Marijuana.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    row_num = 1
    for row in reader:
        licenseNumber = row['LicenseNumber'].strip()
        licenseType = row['LicenseType']
        licenseStatus = row['LicenseStatus'].replace(' ', '_')
        businessName = row['BusinessName'].replace(' ', '_')
        locationStreetAddress = row['LocationStreetAddress']
        locationCity = row['LocationCity'].replace(' ', '_')
        locationState = row['LocationState'].replace(' ', '_')
        locationZip = row['LocationZip']
        locationCounty = row['LocationCounty'].replace(' ', '_')
        designatedRepresentativeLicenseNumber = row['Designated Representative License Number'].replace(' ', '_')
        designatedRepresentative = row['Designated Representative'].replace(' ', '_')
        # Creating URI for the marijuana.
        #identifying the each marijuana with the unique license number
        
        marijuana_uri = pfs["kl-res"][licenseNumber]

        #creating uris for location
        state_uri = pfs["kl-res"][locationState]
        city_uri = pfs["kl-res"][locationCity]
        county_uri = pfs["kl-res"][locationCounty]
        #State uri
        g.add((state_uri, a, State))
        g.add((state_uri,  hasName, Literal(locationState.replace('_', ' ').replace(',',''),datatype=XSD.string)))
        #city uri
        g.add((city_uri, a, City))
        g.add((city_uri,  hasName, Literal(locationCity.replace('_', ' ').replace(',',''),datatype=XSD.string)))
        #country uri
        g.add((county_uri, a, County))
        g.add((county_uri,  hasName, Literal(locationCounty.replace('_', ' ').replace(',',''),datatype=XSD.string)))

        #creating triples for marijuana location
        g.add((marijuana_uri, residesInState, state_uri))
        g.add((marijuana_uri, residesInCounty, county_uri))
        g.add((marijuana_uri, residesInCity, city_uri))
        # Adding triples related to the business
        g.add((marijuana_uri, a,Marijuana))
        g.add((marijuana_uri, hasLicenseType, Literal(licenseType,datatype=XSD.string)))
        g.add((marijuana_uri, isLicenseStatus, Literal(licenseStatus,datatype=XSD.string)))
        g.add((marijuana_uri, hasAddress, Literal(locationStreetAddress,datatype=XSD.string)))
        
        # Representing representative as person
        representative_uri = pfs["kl-res"][designatedRepresentative]
        g.add((representative_uri, a,Person))
        g.add((representative_uri, hasName, Literal(designatedRepresentative.replace('_', ' ').replace(',',''),datatype=XSD.string)))
        g.add((marijuana_uri, hasRepresentative, representative_uri))
        g.add((representative_uri, hasLicense, Literal(designatedRepresentativeLicenseNumber,datatype=XSD.string)))
        # Defining business name as Organization
        business_uri = pfs["kl-res"][businessName]
        g.add((business_uri, a,Organization))
        g.add((business_uri, hasName, Literal(businessName.replace('_', ' ').replace(',',''),datatype=XSD.string)))
        g.add((business_uri, hasId,marijuana_uri))
        g.add((marijuana_uri, hasBusinessName,business_uri))
        g.add((marijuana_uri, hasLabel,Literal(businessName.replace('_', ' ').replace(',',''),datatype=XSD.string)))


# Define the output folder and file name
output_folder = "output"
output_file = os.path.join(output_folder, 'marijuana_knowledge_graph.ttl')

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created successfully.")

# Serialize the RDF graph and store in the output file
temp = g.serialize(format="turtle", encoding="utf-8", destination=output_file)
print(f"File '{output_file}' created in the output folder.")



