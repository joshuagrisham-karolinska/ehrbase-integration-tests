# Copyright (c) 2019 Wladislaw Wagner (Vitasystems GmbH), Pablo Pazos (Hannover Medical School).
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



*** Settings ***

Documentation   General setting for OpenEHR test suites.
# Metadata    Version        1.0

# Bring in variables from arguments / env / file before anything else
Variables   variables/sut_config.py

Library     REST    ${BASEURL}    ssl_verify=${SSL_VERIFY}
Library     RequestsLibrary  WITH NAME  R
Library     String
Library     Collections
Library     OperatingSystem
Library     Process
Library     XML
Library     JSONLibrary
Library     DateTime
Library     DatabaseLibrary
Library     distutils.util
Library     MockServerLibrary

Library     libraries/dockerlib.py
Library     libraries/jsonlib.py
Library     libraries/token_decoder.py
Library     libraries/composition_validation_lib.py
# These we have already loaded above with sut_config.py
# Library     variables/get_global_configs.py
# Variables   variables/additional_configs.yml

Resource    keywords/generic_keywords.robot
# These has been moved to first in the list
# Variables   variables/sut_config.py
# ...         ${SUT}    ${AUTH_TYPE}    ${NODOCKER}

# TODO: follow up references to variables below so that everything which makes sense will come from get_global_configs / sut_config


*** Variables ***
${PROJECT_ROOT}          ${EXECDIR}${/}..
${POM_FILE}              ${PROJECT_ROOT}${/}pom.xml
${CREATING_SYSTEM_ID}    ${NODENAME}
${SMOKE_TEST_PASSED}     ${TRUE}

${CODE_COVERAGE}         False
${NODOCKER}              False
${REDUMP_REQUIRED}       ${FALSE}
${ALLOW-TEMPLATE-OVERWRITE}    ${TRUE}
${CACHE-ENABLED}         ${TRUE}


*** Keywords ***
