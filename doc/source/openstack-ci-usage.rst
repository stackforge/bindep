======================
Bindep in OpenStack CI
======================

The OpenStack CI infrastructure will install packages marked for a
profile (see :ref:`Profiles`) named "test" along with any packages belonging
to the default profile. This allows projects to document their run
time dependencies - the default packages - and the additional packages
needed for testing.

Note that bindep is not used by devstack based tests, those have their
own way to document binary dependencies.
