# Karolinska openEHR Tests

See: https://docs.ehrbase.org/en/latest/03_development/02_testing/index.html

```sh
# Start EHRBase and a container with our test robot in it
docker-compose up --build --detach

# Open up a bash prompt in the test robot container
docker exec -it robot bash -l

export OPENEHR_NAME=ehrbase
export RESULTS_ROOT=/tests/results/$OPENEHR_NAME/`date --utc +%Y%m%dT%H%M%SZ`

# Create an array of all but QUERY_SERVICE tests (since two tests use the same test but with a tag filter set)
declare -a TEST_NAMES=("composition" "contribution" "directory" "ehr_service" "ehr_status" "knowledge" "sanity" "template" "query" "cors")

# Run the QUERY_SERVICE tests separately:
t=query_service_empty && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} -i aql_empty_db robot/QUERY_SERVICE_TESTS
t=query_service_loaded && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} -i aql_loaded_db robot/QUERY_SERVICE_TESTS

# Run all other tests one at a time:
t=composition && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=contribution && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=directory && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=ehr_service && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=ehr_status && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=knowledge && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=sanity && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=template && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=query && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
t=cors && \
  robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS

# Or run all of the tests using a loop:
#for t in "${TEST_NAMES[@]}"
#do
#    robot -d $RESULTS_ROOT/$t -e future -e circleci -e TODO -e obsolete -e libtest -L TRACE --noncritical not-ready --name ${t^^} robot/${t^^}_TESTS
#done

# Copy results index template to results folder
cp /results-index.html $RESULTS_ROOT/index.html

# Exit the test robot container
exit

# Shutdown the Docker Compose stack
docker-compose down
```

If you want to run against another environment, one way is to change the environment variables. For example:

```sh
export PORT="443"
export BASEURL="https://some-other-url/..."
export ECISURL=""
export ADMIN_BASEURL=""
export HEARTBEAT_URL=""
export NODENAME="some-other-system"
export CONTROL_MODE="NONE"
export SSL_VERIFY="False"

export OPENEHR_NAME=some-other-system
export RESULTS_ROOT=/tests/results/$OPENEHR_NAME/`date --utc +%Y%m%dT%H%M%SZ`
```
