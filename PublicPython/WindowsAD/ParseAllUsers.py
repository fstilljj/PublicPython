import ldap3
from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES

# Replace with your AD server, bind DN, and password
server = ldap3.Server('10.33.30.40', get_info=ldap3.ALL)
conn = ldap3.Connection(server, user='astepiko@domain.ru', password='Ciscoal1')

# Base DN for user search
base_dn = 'DC=domain,DC=ru'

# Search filter for users
search_filter = '(objectCategory=person)'

# Attributes to retrieve
attributes = ['samaccountname', 'displayname', 'userprincipalname', 'description']  # Adjust as needed

def get_all_users():
    users = []
    page_size = 1000  # Adjust page size as needed

    with conn as c:
        c.bind()
        c.search(base_dn, search_filter, search_scope=SUBTREE, attributes=attributes, paged_size=page_size)
        for entry in c.response:
            if entry['type'] != 'searchResEntry':
                continue
            users.append(entry['attributes'])

    return users

if name == 'main':
    all_users = get_all_users()
    for user in all_users:
        print(user)