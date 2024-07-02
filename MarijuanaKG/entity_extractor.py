import rdflib
#from rdflib import Graph, URIRef, Namespace
from rdflib import OWL, RDF, RDFS, XSD, TIME
g = rdflib.Graph()

g.parse("marijuana_knowledge_graph.ttl", format="turtle")

resource_url = "http://kastle-lab.org/lod/resource/"
ontology_url = "http://kastle-lab.org/lod/ontology/"

kl_ont = rdflib.Namespace(f"{ontology_url}")
kl_res = rdflib.Namespace(f"{resource_url}")


def retrieve_dispensary_details(dispensary_names, graph=g):
    statements = []

    # Iterate through the provided dispensary names
    for name in dispensary_names:
        # Query the graph for dispensaries with the given business name
        query = rdflib.URIRef(f"{resource_url}{name}")
        for dispensary in graph.subjects(kl_ont.hasBusinessName, query):
            dispensary_name = graph.value(dispensary, RDFS.label, None)
            address = graph.value(dispensary, kl_ont.hasAddress, None)
            #license_type = graph.value(dispensary, kl_ont.hasLicenseType, None)
            representative = graph.value(dispensary, kl_ont.hasRepresentative, None)
            #storing name
            representative = graph.value(representative, kl_ont.hasName, None)
            license_status = graph.value(dispensary, kl_ont.isLicenseStatus, None)
            # city details
            city = graph.value(dispensary, kl_ont.residesInCity, None)
            city = graph.value(city, kl_ont.hasName, None)
            #county details
            county = graph.value(dispensary, kl_ont.residesInCounty, None)
            county = graph.value(county, kl_ont.hasName, None)
            #state
            state = graph.value(dispensary, kl_ont.residesInState, None)
            state = graph.value(state,  kl_ont.hasName, None)

            statement = f"{dispensary_name} is a marijuana dispensary located at {address} in {city}, {county}, {state}. The representative is {representative} and the license status is {license_status}."
            statements.append(statement)

    return statements

def remove_special_chars(input_list):
    modified_list=[]
    for item in input_list:
        modified_list.append(item.replace(' ', '_'))
    return modified_list 



