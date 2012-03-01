from openbudget.settings import *
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType,GroupOfNamesType
import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)




# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://macmini.cochranedavey.private"

#AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=com"
#AUTH_LDAP_BIND_PASSWORD = "phlebotinum"
AUTH_LDAP_USER_SEARCH = LDAPSearch("CN=users,DC=macmini,DC=cochranedavey,DC=private",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# or perhaps:
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,CN=users,DC=macmini,DC=cochranedavey,DC=private"

#AUTH_LDAP_START_TLS = True


# Set up the basic group parameters.
#AUTH_LDAP_GROUP_SEARCH = LDAPSearch("cn=groups,DC=macmini,DC=cochranedavey,DC=private",
#    ldap.SCOPE_SUBTREE, "objectClass=PosixGroup" 
#
#)
#AUTH_LDAP_GROUP_TYPE = PosixGroupType() #GroupOfNamesType(name_attr="cn")
#AUTH_LDAP_MIRROR_GROUPS = True 

# Simple group restrictions
#AUTH_LDAP_REQUIRE_GROUP = "CN=cochranedavey,ou=groups,DC=macmini,DC=cochranedavey,DC=private"
#AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

#AUTH_LDAP_PROFILE_ATTR_MAP = {
#    "employee_number": "employeeNumber"
#}

#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    #"is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=cochranedavey,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}

#AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
#AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600



DEBUG = True


DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'openbudget.db'
