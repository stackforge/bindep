======================
Bindep in OpenStack CI
======================

The OpenStack CI infrastructure uses the "test" profile for
installation of packages. This allows projects to document their run
time dependencies - the default packages - and the additional packages
needed for testing.

Note that bindep is not used by devstack based tests, those have their
own way to document binary dependencies.
