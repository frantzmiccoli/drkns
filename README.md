drkns is a simple build tool aimed at easing the continuous integration of 
monorepos through dependency aware caching.

[![Build Status](https://github.com/frantzmiccoli/drkns/actions/workflows/main.yml/badge.svg)](https://github.com/frantzmiccoli/drkns/actions)

Le problem
===

Monorepositories contain many projects, it rarely makes sense to
rebuild an every projects when changes are committed.

But we can't build necessarily limit ourselves to run builds and tests 
in directories where changes occurred because some projects depends on others.

Caveat
===

No parallel execution.

Quick start
===

> You wild kid!
> 
> &nbsp;&nbsp;&nbsp;&nbsp;*Confucius*

Check [a dummy project](https://github.com/frantzmiccoli/drkns/tree/master/testprojects/nominalcase) 
on which our tests are based.

Create your drkns.yml files
---

From your monorepo root, in `drkns.yml`:

```
dependencies:
  project1: projects/project1
  project2: projects/project2
  library1: library/library1
```

Sample `projects/project1/drkns.yml`:

```
checkSteps:
  installDependencies: pipenv install
  test: pipenv run pytest
buildSteps:
  build: pipenv run paver build
  deploy: pipenv run paver deploy_to_pypi
dependencies:
  - ../../library/library1
```

Test that everything is alright
---


```
drkns check  # Check the configuration file
drkns list   # Check list the identified steps
drkns run    # Run everything
```

`.gitignore` hygiene
---

```
echo '.drknspersistence/*' >> .gitignore
```

In your CI
---

With environment variables:
* DRKNS_S3_PATH: S3 path to a directory you can write to
* AWS_ACCESS_KEY_ID 
* AWS_DEFAULT_REGION
* AWS_SECRET_ACCESS_KEY

```
pip install drkns

drkns check             # We never know
drkns sync in           # Get past execution statuses from S3
drkns debug             # If needed, you can check which steps are
                        #   going to run here
drkns run               # Run all steps
drkns clean             # Will remove one week old execution statuses to 
                        #   limit disk usage
drkns sync out --delete # Persist all execution statuses from S3,
                        #  **use --delete** to also delete data removed by 
                        #  `clean`
```

Documentation
===

Unit
---

Each `drkns.yml` forms a `unit`, it should represent a specific unit of your 
code, a directory containing a lib or a project, that has specific build steps
or can be depended on.

`drkns.yml` accepted fields:

* `directory`: string, Current directory by default, only used to compute the 
   hash associated with this build file
* `dependencies`: strings sequence, path containing another `drkns.yml` file 
  to load, you can also only indicate a directory name. 
* `checkSteps`: dictionary of steps, see below.
* `buildSteps`: dictionary of steps, see below.
* `cleanupSteps`: dictionary of steps, see below.

Steps
---

Steps :

* Have a `command` to run, string, required.
* Have a `background` flag, default to false.
* Can also be a single string, the `command` argument.
* Are ordered.
* Are deduplicated at execution. E.g. `library/front-util/drkns.yml` is required
   by both `projects/aviation-customer/drkns.yml` and 
   `projects/retail-customer/drkns.yml` it will only appear in the first one to
   be parsed. Note that this can impact `.gitignore` resolution.

Three different step types are available, by order of execution:

1. `checkSteps`: steps necessary to check the integrity of the `unit`. 
    Will always be ran if no checkSteps has already failed in this `unit`.
    Typically used to build
    your application, your docker images and run your unit tests.
    If a steps fail, the following ones will not be executed.
2. `buildSteps`: steps executed only if `checkSteps`, dependencies' `checkSteps`
    and previous buildSteps succeeded. You
    can use this to upload or deploy the build artifacts. Beware there is no
    guarantee that `dependencies` will be executed, there execution might have
    been started 
3. `cleanupSteps`: steps executed no matter what (except if the `unit` has not 
   changed since last execution). You can suppress things that have
    taken too much memory or things in the like.

### Warning: implicit cleanup of background tasks

If any of your steps used the background attributes they are killed after the 
cleanup steps at the end of the execution of your `unit.

### Caching

The point of `drkns` is to not rerun everything for every change.

Upon execution a `.drknspersistence` folder in the directory of each unit will 
be created, this folder will contain the execution status of each step for a 
specific unit, step and a specific hash.

At each execution a hash for the unit is computed, it changes if files within
the unit or its dependencies hashes have changed. If it is present in the
persisted files, it will prevent the execution.

### Ignoring files `.drknsignore`

Often, it happens that the execution of steps will alter some files in the 
directory changing the mentioned above hash.

It is not necessarily something that we wish.

You can add partial or full file or directory names (as long as they have a 
trailing `/`) to be ignored in a `.drknsignore` file. A unit will ignore
specific patterns.

**Warning: `.drknsignore` are also inherited from parents.** Because of this 
path are not supported to avoid ambiguity.

The ignored elements are passed to `dirhash`'s `ignore` argument. The relevant 
documentation is available at https://pypi.org/project/dirhash/ .

Sample `.drknsignore`:

```
*.tmp
build/
```

### Persistence

Persistence is enabled through S3 buckets.

You need a `DRKNS_S3_PATH` environment variable, or provide it as a command line
argument.

`export DRKNS_S3_PATH=s3://some-drkns-bucket/someProjectDirectory`

`drkns` expects [AWS environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) 
to be defined: `AWS_ACCESS_KEY_ID`, `AWS_DEFAULT_REGION` and 
`AWS_SECRET_ACCESS_KEY` for the AWS client to work properly.

### Parallel CI Generation

This is an advanced usage. You are invited to skip this if this is your first 
dive in `drkns`.

Once your CI is setup, maybe you want to parallelize job execution, `drkns` can 
generate your CI configuration provided you write a template.

The template must be located at `.drknsgeneration/*.template.*`, only a single
template file must be in this directory. 

Fields to be defined in the template, always in the form `%FIELD_NAME%`:

* `DRKNS_GROUP_BEGIN` and `%DRKNS_GROUP_END%`: around a group template 
  definition. A group will contain `units` that are
  ran together. The lines containing those tags will be removed. For now, only
  one unit per group is supported, so do not be surprised.
* `DRKNS_UNIT_BEGIN` and `DRKNS_UNIT_END`: around a unit template, 
  mostly calling `drkns run %DRKNS_UNIT_NAME%`. The lines containing those tags 
  will be removed.
* `%DRKNS_GROUP_UNITS%`: where group units will be inserted - 
  must be within a group template. The line containing this tag will be removed.
* `%DRKNS_UNIT_NAME%`: the unit's name
* `%DRKNS_DEPENDENCY_GROUPS_NAMES{, }%`: the dependency group names, 
  with a comma separator (as an example),
  if you need a 
  separator: `%DRKNS_DEPENDENCY_GROUPS_NAMES?{, }%` will only insert a `, `.
* `%DRKNS_ALL_GROUPS_NAMES{, }%`: all group names, here with a comma separator

`drkns` CLI
---

### Commands

* `drkns check`: checks `drkns.yml` files by loading the one in the current
   directory and printing errors if anything bad happens.
* `drkns clean`: cleans older than a week execution steps from the persisted 
  data.
* `drkns debug`: prints debug information, mostly to control if execution cache
  has been altered.
* `drkns forget UNIT_NAME`: forgets the previous execution of `UNIT_NAME`,
   `all` for everything. Nota the name of the root config unit is `main`. This
   can be used to force the new execution of some entries.   
* `drkns list`: prints all the available steps plan. Beware repeating steps are 
   removed.
* `drkns run [--limit-output] [--force-success] [--summary] STEP_NAME`: run the
   given steps and its requirements or all steps.
* `drkns sync DIRECTION [--delete ][DRKNS_S3_PATH]`: syncs the persisted 
  execution cache, `DIRECTION` can be `in` or `out`.
* `drkns generate`: generates a file based on the template described above
  
### Options

* `--force-success`: flag, forces exit code `0`.
* `--limit-output`: flag, less restrictive than `summary`, limits the outputs to
  the failed steps' output at this execution (ignored cached ones), steps and
  execution statuses.
* `--summary`: flag, prints only the summary: steps and execution statuses.
* `--delete`: flag, deletes remote execution status files that do not exist 
  locally. It is of paramount importance to use after `clean`. It is a flag as
  it makes sense to sync in / sync out at each step to prevent duplicate 
  execution when a parallel processing is happening or the process can be 
  canceled.

Output
---

`drkns` output is composed of the failed steps output only and a summary.

### Failed steps output

```
Output for unitName1@stepName1:
/bin/sh: line 1: stop: command not found
```

In case a step got canceled because of a previous failure:

```
Output for unitName2@stepName2:
Previous failure of dependency1 / dependency1FailingCheck
```

### Summary

```
dependency1@dependency1FailingCheck: Error (restored)
dependency1@dependency1Build: Ignored
dependency1@dependency1Cleanup: OK (restored)
project1@project1Check: OK (restored)
project1@project1ShouldNotRunBuild: Ignored (restored)
project1@project1Cleanup: OK (restored)
project3@project3Build: OK
project3@project3failingCleanup: Error
project3@project3NeverExecutedCleanUp: OK
main@mainCheck1: OK
main@mainBuild1: Ignored
```

Step statuses:

* `Error`: an error occurred on execution
* `Ignored`: an error occurred in a previous step, preventing this step from 
  being executed
* `OK`: all good

`(restored)` indicates that the execution did not happen this round but was
cache from a previous step.
