import ldap3
from ldap3 import Server, Connection, MODIFY_REPLACE

def disable_ad_user(server, bind_dn, password, user_dn):
  """Disables a user in Active Directory.

  Args:
    server: The LDAP server address.
    bind_dn: The bind DN for authentication.
    password: The password for the bind DN.
    user_dn: The distinguished name of the user to disable.
  """

  conn = ldap3.Connection(server, user=bind_dn, password=password)
  try:
    conn.bind()

    # Calculate the new userAccountControl value (assuming the user is not already disabled)
    entry = conn.search(user_dn, '(objectCategory=person)', attributes=['userAccountControl'])
    print(conn.response)
    new_control = '514'

    # Modify the userAccountControl attribute
    mod_attrs = {
      'userAccountControl': [(MODIFY_REPLACE, [new_control])]
    }
    result = conn.modify(user_dn, mod_attrs)
    if not result:
      raise Exception(f"Failed to disable user {user_dn}: {conn.result}")
    else:
      print(f"User {user_dn} disabled successfully.")
  finally:
    conn.unbind()

# Example usage:
server = '10.33.30.40'
bind_dn = 'astepiko@domain.ru'
password = 'Ciscoal1'
user_dn = 'CN=Lev Kukin,OU=Accountant,DC=domain,DC=ru'

disable_ad_user(server, bind_dn, password, user_dn)