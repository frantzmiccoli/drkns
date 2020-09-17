Features
===

1. Ability to get a hash from a directory, this will enable to know when a 
directory has changed since last build.
2. Dependency between build processes
3. Step by step execution
4. Steps with hash form a key, their previous execution is recorded
5. Persistence and restoration with AWS S3 is supported

Notes
===

One of the problem is to still have the different steps split, but actually 
scripting the different steps to be called manually and calling it all from
a master build file should do it. Every step is self cancelled if the build 
has not reason to be ran (already executed).

CLI interface
===

The command line interface offers the following commands :

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

# Clean persisted data older than a week old (to not overload the cache after 
# too many builds)
drkns clean

# Persist previous execution information from S3, see assumptions for sync in
# Beware this erase extra files 
drkns sync out
```

Sample master yml
===

drkns.yml

```yml
dependencies:
  sub1: subProject1/drkns.yml
  

```

Sample dependency yml
===


subProject1/drkns.yml

```yml
steps:
  buildImages: |
       docker build -q -t ...
       
  startContainers: "docker run --network host --name test -d backServer-test"
```

yml reference
===

* `directory` : Current directory by default, only used to compute the hash associated with this build file
* `steps`: ordered and named commands.
* `dependencies`: named external drkns yml to load, their steps becomes callables through `drkns dependencyName:stepName`