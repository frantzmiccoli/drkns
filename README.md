drkns is a simple monorepo build tool.

[![Build Status](https://api.travis-ci.org/frantzmiccoli/drkns.png)](http://travis-ci.org/frantzmiccoli/drkns)

Build is driven through YAML files, that can have dependencies over other YAML
files.

* Steps are built after the dependencies.
* A failure at a step prevents the execution of the next one.
* The result of each execution step, if a directory is left unchanged no
execution will be triggered again. 
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
steps:
  buildImages: |
       docker build -q -t ...
       
  startContainers: "docker run --network host --name test -d backServer-test"
```

YAML reference
===

* `directory` : Current directory by default, only used to compute the hash 
associated with this build file
* `dependencies`: named external drkns yml to load, their steps becomes 
callables through `drkns dependencyName.stepName`
* `steps`: ordered and named commands. Commands are either a string, or have two
keys: `command` (string)  and `background` (bool default false)
* `cleanUpSteps`: same as `steps`, but those are executed no matter the 
execution of the previous ones. 

CLI interface
===

The command line interface offers the following commands:

```
# Checks that the configuration makes sense (no output is a good sign
drkns check

# List all steps
drkns list

# Restore previous execution information from S3
# Assuming an environment variable DRKNS_S3_PATH exists under the form 
# "s3://buck3t/d1r" 
drkns sync in

# also available for something like
# drkns sync in s3://buck3t/d1r

# Runs all steps
drkns run 

# Runs first step
drkns run 1

# Runs identified task
drkns run sub1.buildImages

# Runs all steps but returns 0 no matter what happens 
drkns run --force-success

# Return the last `drkns run` execution status (useful in combination with 
# drkns run --force-success
drkns laststatus

# Clean persisted data older than a week old when there is more than a few
# (to not overload the cache after too many builds)
drkns clean

# Persist previous execution information from S3, see assumptions for sync in
# Beware this erase extra files 
drkns sync out
```
