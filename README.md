drkns is a simple build tool aimed at easing the continuous integration of 
monorepos through the use of caching.

[![Build Status](https://github.com/frantzmiccoli/drkns/actions/workflows/main.yml/badge.svg)](https://github.com/frantzmiccoli/drkns/actions)

Build is driven through YAML files, that can have dependencies over other YAML
files.

* Steps are built after the dependencies.
* A failure at a step prevents the execution of the next one.
* The result of each execution step is cached, if a directory is left unchanged 
  no execution will be triggered again. 
* State can be persisted in Amazon S3 to have a shared memory between volatile
build instances


Sample master drkns.yml
===

drkns.yml

```yml
dependencies:
  sub1: subProject1/drkns.yml
  

```

Sample dependency drkns.yml
===


subProject1/drkns.yml

```yml
checkSteps:
  buildImages: |
       docker build -q -t ...
       
  startContainers: "docker run --network host --name test -d backServer-test"
```

YAML reference
===

* `directory`: Current directory by default, only used to compute the hash 
associated with this build file
* `dependencies`: named external drkns yml to load, their steps becomes 
callables through `drkns dependencyName.stepName`
* `checkSteps`: ordered and named commands. Commands are either a string, 
  or have two keys: `command` (string)  and `background` 
  (bool default false)
* `buildSteps`: same as `checkSteps`, but those are executed only if 
  `checkSteps` and dependencies' `checkSteps` got processed without errors. 
* `cleanUpSteps`: same as `checkSteps`, but those are executed no matter the 
execution of the previous ones. 

CLI interface
===

The command line interface offers the following commands:

```
# Checks that the configuration makes sense (no output is a good sign
drkns check

# List all steps
drkns list

# Print debug information
drkns debug

# Restore previous execution information from S3
# Assuming an environment variable DRKNS_S3_PATH exists under the form 
# "s3://buck3t/d1r" 
drkns sync in

# also available for something like
# drkns sync in s3://buck3t/d1r

# Runs all steps
drkns run 

# Runs identified task
drkns run sub1.buildImages

# Runs all steps but returns 0 no matter what happens 
drkns run --force-success

# Return the last `drkns run` to get the execution status 
drkns run

# Limit output to failed and non restored or ignored entities 
drkns run --limit-output

# Willing to have only the step statuses and not the failed output 
drkns run --summary

# Clean persisted data older than a week old when there is more than a few
# (to not overload the cache after too many builds)
drkns clean

# Persist previous execution information from S3, see assumptions for sync in
# Beware this erase extra files 
drkns sync out
```
