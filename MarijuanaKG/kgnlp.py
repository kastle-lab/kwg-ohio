import rdflib

g = rdflib.Graph()

g.parse("marijuana_knowledge_graph.ttl", format="turtle")

kl_ont = rdflib.Namespace("http://kastle-lab.org/lod/ontology/")
kl_res = rdflib.Namespace("http://kastle-lab.org/lod/resource/")

def generate_statements(graph):
    statements = []

    for dispensary, _, _ in graph.triples((None, rdflib.RDF.type, kl_ont.Marijuana)):
        business_name = graph.value(dispensary, kl_ont.hasBusinessName, None)
        address = graph.value(dispensary, kl_ont.hasAddress, None)
        license_type = graph.value(dispensary, kl_ont.hasLicenseType, None)
        representative = graph.value(dispensary, kl_ont.hasRepresentative, None)
        license_status = graph.value(dispensary, kl_ont.isLicenseStatus, None)
        city = graph.value(dispensary, kl_ont.residesInCity, None)
        county = graph.value(dispensary, kl_ont.residesInCounty, None)
        state = graph.value(dispensary, kl_ont.residesInState, None)
        # replacing
        business_name = business_name.replace('_', ' ')
        business_name = business_name.replace(',', '')
        representative = representative.replace('_',' ')
        city = city.replace('_', ' ')
        county = county.replace('_', ' ')
        state = state.replace('_','')
        
        old_kl_res = 'http://kastle-lab.org/lod/resource/'
        new_kl_res = ''
        business_name = business_name.replace(old_kl_res, new_kl_res)
        representative = representative.replace(old_kl_res, new_kl_res)
        # capitalizing words
        business_name = business_name.title()
        representative = representative.title()
        #
        statements.append(f"Question: Is  {business_name} a marijuana dispensary? Answer: Yes, {business_name} is a marijuana dispensary located at {address}.")
        statements.append(f"Question: Is  {address}, an address? Answer: Yes, {address} is a address in {state} where {business_name} is located.")
        statements.append(f"Question: What is the address of marijuana dispensary {business_name}? Answer: {business_name} is a marijuana dispensary located at {address}.")
        statements.append(f"Question: Where is {business_name} dispensary located? Answer: {business_name} dispensary is located at {address}.")
        statements.append(f"Question: What is the license type of marijuana dispensary {business_name}? Answer: {business_name} operates under a {license_type}.")
        statements.append(f"Question: What's the license type of marijuana dispensary {business_name}? Answer: dispensary {business_name} operates under a {license_type}.")
        statements.append(f"Question: Who is the representative of marijuana dispensary {business_name}? Answer: The representative for {business_name} is {representative}.")
        statements.append(f"Question: Which marijuana dispensary is represented by {representative}? Answer: The marijuana dispensary represented by {representative} is {business_name}")
        statements.append(f"Question: Is {representative} the representative of marijuana dispensary {business_name}? Answer: Yes, {representative} is the representative of {business_name}.")
        statements.append(f"Question: Who is the representing marijuana dispensary {business_name}? Answer: The representative for {business_name} is {representative}.")
        statements.append(f"Question: {business_name} is represented by whom? Answer: The representative for {business_name} is {representative}.")
        statements.append(f"Question: {business_name} is represented by whom? Answer: The {business_name} is represented by {representative}.")
        statements.append(f"Question: What is the license status of {business_name}? Answer: The license status of {business_name} is currently {license_status}.")
        statements.append(f"Question: What is the county {business_name} dispensary is setup? Answer: {business_name} is based in County: {county}.")
        statements.append(f"Question: What is the state {business_name} dispensary is setup? Answer: {business_name} is based in State: {state}.")
        statements.append(f"Question: What is the city {business_name} dispensary is setup? Answer: {business_name} is based in City: {city}.")
        statements.append(f"Question: what is {city}? Answer: {city} is a city in the {county} County, {state}.")
        statements.append(f"Question: what is {county}? Answer: {county} is a county in {state}.")
        statements.append(f"Question: In which city {business_name} dispensary is located? Answer: {business_name} is located in {city} city.")
        statements.append(f"Question: In which county {business_name} dispensary is located? Answer: {business_name} is located in {county} county.")
        statements.append(f"Question: Where is {business_name} dispensary located Answer: {business_name} is based in City: {city}, County: {county}, State: {state}.")

    return statements

statements = generate_statements(g)
output_file_path = "marijuana_nlp.txt"

with open(output_file_path, 'w') as output_file:
    for statement in statements:
        output_file.write(statement + "\n") 

file_path = output_file_path

old_kl_res = 'http://kastle-lab.org/lod/resource/'
new_kl_res = ''

old_kl_ont = 'http://kastle-lab.org/lod/ontology/'
new_kl_ont = ''

with open(file_path, 'r') as file:
    file_contents = file.read()

# Replace the pattern
modified_contents = file_contents.replace(old_kl_res, new_kl_res)
modified_contents = modified_contents.replace(old_kl_ont, new_kl_ont)
# Write the modified contents back
with open(file_path, 'w') as file:
    file.write(modified_contents)

print(f"Statements written to {output_file_path}")
