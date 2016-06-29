Backward-Incompatible Changes Between 1.0.0 and 2.0.0
=====================================================

The following behavior changes between the 1.0.0 and 2.0.0 releases
break backward compatibility:

 * Running under Python 2.6 is no longer officially supported
 * Platform profiles are now treated as a "logical AND" (as opposed
   to user profiles which are still treated as a "logical OR")
