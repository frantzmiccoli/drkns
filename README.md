To do
===

1. Implementation clean up --> more service oriented
2. Use sys.POpen instead of paver.easy.sh
3. S3 synchronization  

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

One of the problem is to still have the different step splitted, but actually scripting the different steps to be called manually and calling it all from a master build file should do it. Every step is self cancelled if the build has not reason to be ran (already executed).

CLI interface
===

```
# Checks that the configuration makes sense
drkns check

# Runs all steps
drkns run 

# Runs first step
drkns run 1

# Runs identified task
drkns run sub1:buildImages
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
       
  startContainers: "docker run --network host --name test -d nxback-test"
  

```

yml reference
===

* `directory` : Current directory by default, only used to compute the hash associated with this build file
* `steps`: ordered and named commands.
* `dependencies`: named external drkns yml to load, their steps becomes callables through `drkns dependencyName:stepName`