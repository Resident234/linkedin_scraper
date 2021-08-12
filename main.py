from pprint import pprint
from linkedin_api import Linkedin
# Authenticate using any Linkedin account credentials
api = Linkedin('yuya2849kyoto@gmail.com', 'ionazunn3542')

# GET a profile
profile = api.get_profile('yuyafukuchi261a861b1')
pprint(profile)
# GET a profiles contact info
contact_info = api.get_profile_contact_info('yuyafukuchi261a861b1')
pprint(contact_info)
# GET 1st degree connections of a given profile
connections = api.get_profile_connections('risa-s-832092176')
pprint(connections)

