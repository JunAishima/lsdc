GUI markings

* current request is 99999
  * color = green
* priority > 0
  * color = white
  * checked
  * currently in queue
* priority < 0
  * color = cyan
  * not checkable
  * not in queue - done
* else of above
  * color = white
  * unchecked

How it functions
* to move up, add 10
* to move down, subtract 20
* make it top, add 100 to current maximum
* make it bottom, subtract 100 from current minimum

the above suggests that they are automatically stepped at 10 or 20

Other info
* default escan - 5000
* new load, centered sample - 5000
* new collection in addSampleRequestCB, autocentered - 5000
* multi request location - 6000
