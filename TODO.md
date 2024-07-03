For later:

* Parallel execution would need: 
  * a dependency aware execution plan
  * a runner that uses threads
  * a status history that doesn't work as a list (because we rely on the order
    of elements here)

* Live output (easier):
  * Generate events on step execution status creation
  * Generate a event to signal end of global execution and trigger an output
    flush

* Forget should print a warning if nothing has been erased
