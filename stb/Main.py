query_engine = index.as_query_engine()
response = query_engine.query("Graduate and Fresh Graduate programmes at STB")
print(response)
print("SOURCE +++++++>>>>>>",response.get_formatted_sources)