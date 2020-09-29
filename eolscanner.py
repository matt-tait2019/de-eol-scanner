import logging
from dotenv import load_dotenv
#Set up initial logger config
# logging.basicConfig(filename='/var/log/slvrcld/quote-linker.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
load_dotenv()

# from db.dbapi import ProductDbApi
from deapiinterface import SemiStructuredProductInterface

"""
This is an EOL Scanner for testing/demo only
It simply scans through and marks any product without a quote as EOL
"""

api_interface = SemiStructuredProductInterface('cdf4a95fc10cec2568dd9e7c5736ea677b4f5bd9', 'http://localhost:5000/graphql')


end_of_life_products = api_interface.get_structured_products(category='smartphones', brand='Apple', has_quotes=0, fields_to_include=['common_name', 'based_on_id', 'series_parent_id', 'id'])


for product in end_of_life_products['products']:
	if product['based_on_id'] == product['series_parent_id']:
		print(f"marking {product['common_name']} as EOL")
		api_interface.update_structured_product(product['id'], status_eol=1)
	else:
		productss = api_interface.get_structured_products(category='smartphones', brand='Apple',
														  id=product['based_on_id'])
		print(f"marking {productss['products'][0]['common_name']} as EOL")
		api_interface.update_structured_product(product['based_on_id'], category='smartphones', status_eol=1)


product_with_quotes = api_interface.get_structured_products(category='smartphones', brand='Apple', has_quotes=1, fields_to_include=['common_name', 'based_on_id', 'series_parent_id', 'id'])

for product in product_with_quotes['products']:
	if product['based_on_id'] == product['series_parent_id']:
		print(f"marking {product['common_name']} as current")
		api_interface.update_structured_product(product['id'], status_eol=0)
	else:
		productss = api_interface.get_structured_products(category='smartphones', brand='Apple', id=product['based_on_id'])
		print(f"marking {productss['products'][0]['common_name']} as current")
		api_interface.update_structured_product(product['based_on_id'], category='smartphones', status_eol=0)
