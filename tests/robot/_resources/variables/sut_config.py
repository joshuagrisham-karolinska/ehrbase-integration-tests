# Copyright (c) 2020 Wladislaw Wagner (www.trustincode.de), (Vitasystems GmbH).
#
# This file is part of Project EHRbase
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import get_global_configs
from requests import request

# TODO: Move almost everything below to their own config INI files (one per environment)

GLOBAL_VARS_FROM_YAML_FUNC = get_global_configs.get_variables()
GLOBAL_PORT_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["GLOBAL_PORT"]
BASEURL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["BASEURL"]
ECISURL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["ECISURL"]
ADMIN_BASEURL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["ADMIN_BASEURL"]
HEARTBEAT_URL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["HEARTBEAT_URL"]
PLUGIN_URL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["PLUGIN_URL"]
RABBITMQ_URL_FROM_YAML = GLOBAL_VARS_FROM_YAML_FUNC["RABBITMQ_URL"]


# KEYCLOAK SETTINGS
HEADER = {"Content-Type": "application/x-www-form-urlencoded"}
KEYCLOAK_URL = "http://localhost:8081/auth"
KC_AUTH_URL = KEYCLOAK_URL + "/realms/ehrbase/protocol/openid-connect/auth"
KC_ACCESS_TOKEN_URL = KEYCLOAK_URL + "/realms/ehrbase/protocol/openid-connect/token"
KC_JWT_ISSUERURI = KEYCLOAK_URL + "/realms/ehrbase"


# SUT CONFIGURATIONS
"""
CONFIG              SUT STARTUP AUTOMATED?      COMMENT
------              ----------------------      -------

DEV                 no                          manually start ehrbase, db
DEV-OAUTH           no                          manually start ehrbase, db, keycloak
TEST                yes
TEST-OAUTH          partly                      manually start keycloak
ADMIN-DEV           no                          manually start ehrbase, db
ADMIN-DEV-OAUTH     manual                      manually start ehrbase, db, keycloak
ADMIN-TEST          yes
ADMIN-TEST-OAUTH    partly                      manually start keycloak
"""

# dev environment: for local development
# requires manual startup of EHRbase and DB
DEV_CONFIG = {
    "SUT": "DEV",
    "GLOBAL_PORT": GLOBAL_PORT_FROM_YAML,
    "BASEURL": BASEURL_FROM_YAML,
    "ECISURL": ECISURL_FROM_YAML,
    "ADMIN_BASEURL": ADMIN_BASEURL_FROM_YAML,
    "HEARTBEAT_URL": HEARTBEAT_URL_FROM_YAML,
    "CREDENTIALS": ["ehrbase-user", "SuperSecretPassword"],
    "SECURITY_AUTHTYPE": "BASIC",
    "AUTHORIZATION": {
        "Authorization": "Basic ZWhyYmFzZS11c2VyOlN1cGVyU2VjcmV0UGFzc3dvcmQ="
    },
    # NOTE: nodename is actually "CREATING_SYSTEM_ID"
    #       and can be set from cli when starting server .jar, i.e.:
    #       `java -jar application.jar --server.nodename=some.foobar.baz`
    #       EHRbase's default is local.ehrbase.org
    "NODENAME": "manual.execution.org",  # CREATING_SYSTEM_ID
    "CONTROL_MODE": "manual",
    "OAUTH_ACCESS_GRANT": {
        "client_id": "ehrbase-client",
        "scope": "openid",
        "username": "ehrbase",
        "password": "ehrbase",
        "grant_type": "password",
    },
    "JWT_ISSUERURI": KC_JWT_ISSUERURI,
    "OAUTH_NAME": "Ehr Base",
    "OAUTH_EMAIL": "ehrbase@ehrbase.org",
    "ACCESS_TOKEN": None,
    "KEYCLOAK_URL": KEYCLOAK_URL,
    "KC_AUTH_URL": KC_AUTH_URL,
    "KC_ACCESS_TOKEN_URL": KC_ACCESS_TOKEN_URL,
    "OAUTH_USER_ROLE": "ehrbase.org/user",
    "OAUTH_ADMIN_ROLE": "ehrbase.org/administrator"
}

# admin-dev environment: for local test of admin interface
# requires manual startup of EHRbase and DB
ADMIN_DEV_CONFIG = {
    "SUT": "ADMIN-DEV",
    "GLOBAL_PORT": GLOBAL_PORT_FROM_YAML,
    "BASEURL": BASEURL_FROM_YAML,
    "ECISURL": ECISURL_FROM_YAML,
    "ADMIN_BASEURL": ADMIN_BASEURL_FROM_YAML,
    "HEARTBEAT_URL": HEARTBEAT_URL_FROM_YAML,
    "CREDENTIALS": ["ehrbase-admin", "EvenMoreSecretPassword"],
    "SECURITY_AUTHTYPE": "BASIC",
    "SPRING_CACHE_TYPE": "SIMPLE",
    "AUTHORIZATION": {
        "Authorization": "Basic ZWhyYmFzZS1hZG1pbjpFdmVuTW9yZVNlY3JldFBhc3N3b3Jk"
    },
    "NODENAME": "local.ehrbase.org",  # CREATING_SYSTEM_ID
    "CONTROL_MODE": "manual",
    "OAUTH_ACCESS_GRANT": {
        "client_id": "ehrbase-client",
        "scope": "openid",
        "username": "admin-robot",  # TODO: recreate exported-keycloak-config to have this user!
        "password": "admin-robot",  #       check README.md in SECURITY_TESTS folder for how to
        "grant_type": "password",
    },
    "JWT_ISSUERURI": KC_JWT_ISSUERURI,
    "OAUTH_NAME": "Admin Ehr Base",
    "OAUTH_EMAIL": "admin-ehrbase@ehrbase.org",
    "ACCESS_TOKEN": None,
    "KEYCLOAK_URL": KEYCLOAK_URL,
    "KC_AUTH_URL": KC_AUTH_URL,
    "KC_ACCESS_TOKEN_URL": KC_ACCESS_TOKEN_URL,
    "OAUTH_USER_ROLE": "ehrbase.org/user",
    "OAUTH_ADMIN_ROLE": "ehrbase.org/administrator"
}

# test environment: used on CI pipeline, can be used locally, too
# handles startup/shutdown of EHRbase and DB automatically
TEST_CONFIG = {
    "SUT": "TEST",
    "GLOBAL_PORT": GLOBAL_PORT_FROM_YAML,
    "BASEURL": BASEURL_FROM_YAML,
    "ECISURL": ECISURL_FROM_YAML,
    "ADMIN_BASEURL": ADMIN_BASEURL_FROM_YAML,
    "HEARTBEAT_URL": HEARTBEAT_URL_FROM_YAML,
    "PLUGINURL": PLUGIN_URL_FROM_YAML,
    "RABBITMQURL": RABBITMQ_URL_FROM_YAML,
    "CREDENTIALS": ["ehrbase-user", "SuperSecretPassword"],
    "SECURITY_AUTHTYPE": "BASIC",
    "SPRING_CACHE_TYPE": "SIMPLE",
    "AUTHORIZATION": {
        "Authorization": "Basic ZWhyYmFzZS11c2VyOlN1cGVyU2VjcmV0UGFzc3dvcmQ="
    },
    "NODENAME": "local.ehrbase.org",  # alias CREATING_SYSTEM_ID
    "CONTROL_MODE": "docker",
    "OAUTH_ACCESS_GRANT": {
        "client_id": "ehrbase-robot",
        "scope": "openid",
        "username": "robot",
        "password": "robot",
        "grant_type": "password",
    },
    "JWT_ISSUERURI": KC_JWT_ISSUERURI,
    "OAUTH_NAME": "Robot Framework",
    "OAUTH_EMAIL": "robot@ehrbase.org",
    "ACCESS_TOKEN": None,
    "KEYCLOAK_URL": KEYCLOAK_URL,
    "KC_AUTH_URL": KC_AUTH_URL,
    "KC_ACCESS_TOKEN_URL": KC_ACCESS_TOKEN_URL,
    "OAUTH_USER_ROLE": "ehrbase.org/user",
    "OAUTH_ADMIN_ROLE": "ehrbase.org/administrator"
}

# admin-test environment: used on CI to test admin interface, can be used locally, too
# handles startup/shutdown of EHRbase and DB automatically
ADMIN_TEST_CONFIG = {
    "SUT": "ADMIN-TEST",
    "GLOBAL_PORT": GLOBAL_PORT_FROM_YAML,
    "BASEURL": BASEURL_FROM_YAML,
    "ECISURL": ECISURL_FROM_YAML,
    "ADMIN_BASEURL": ADMIN_BASEURL_FROM_YAML,
    "HEARTBEAT_URL": HEARTBEAT_URL_FROM_YAML,
    "CREDENTIALS": ["ehrbase-admin", "EvenMoreSecretPassword"],
    "SECURITY_AUTHTYPE": "BASIC",
    "SPRING_CACHE_TYPE": "SIMPLE",
    "AUTHORIZATION": {
        "Authorization": "Basic ZWhyYmFzZS1hZG1pbjpFdmVuTW9yZVNlY3JldFBhc3N3b3Jk"
    },
    "NODENAME": "local.ehrbase.org",  # alias CREATING_SYSTEM_ID
    "CONTROL_MODE": "docker",
    "OAUTH_ACCESS_GRANT": {
        "client_id": "ehrbase-robot",
        "scope": "openid",
        "username": "admin-robot",  # TODO: recreate exported-keycloak-config to have this user!
        "password": "admin-robot",  #       check README.md in SECURITY_TESTS folder for how to
        "grant_type": "password",
    },
    "JWT_ISSUERURI": KC_JWT_ISSUERURI,
    "OAUTH_NAME": "Admin Robot Framework",
    "OAUTH_EMAIL": "admin-robot@ehrbase.org",
    "ACCESS_TOKEN": None,
    "KEYCLOAK_URL": KEYCLOAK_URL,
    "KC_AUTH_URL": KC_AUTH_URL,
    "KC_ACCESS_TOKEN_URL": KC_ACCESS_TOKEN_URL,
    "OAUTH_USER_ROLE": "ehrbase.org/user",
    "OAUTH_ADMIN_ROLE": "ehrbase.org/administrator"
}


# # NOTE: for this configuration to work the following environment variables
# #       have to be available:
# #       BASIC_AUTH (basic auth string for EHRSCAPE, i.e.:
# #                   export BASIC_AUTH="Basic abc...")
# #       EHRSCAPE_USER
# #       EHRSCAPE_PASSWORD
# &{EHRSCAPE}             URL=https://rest.ehrscape.com/rest/openehr/v1
# ...                     HEARTBEAT=https://rest.ehrscape.com/
# ...                     CREDENTIALS=@{scapecreds}
# ...                     BASIC_AUTH={"Authorization": "%{BASIC_AUTH}"}
# ...                     NODENAME=piri.ehrscape.com
# ...                     CONTROL=NONE
# @{scapecreds}           %{EHRSCAPE_USER}    %{EHRSCAPE_PASSWORD}


def get_variables():

    # Instead of everything happening below, we just want to rely on that the user has set everything they want 
    #  in one of the three available config variants (ini file, Environment Variable, or passed as a command argument e.g. --BASEURL)
    result = get_global_configs.get_variables()

    # TODO test if this new "standardized" OAUTH flow below works?
    #  and maybe rename some of the variables to be standardized (OAUTH_ instead of related to Keycloak?)
    if (result["SECURITY_AUTHTYPE"] == 'OAUTH'):
        result["ACCESS_TOKEN"] = request(
            "POST",
            result["KC_ACCESS_TOKEN_URL"],
            headers=HEADER,
            data=result["OAUTH_ACCESS_GRANT"],
        ).json()["access_token"]
        result["AUTHORIZATION"] = {
            "Authorization": "Bearer " + result["ACCESS_TOKEN"]
        }

    return result
