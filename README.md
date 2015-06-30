# Preface #

This document describes the functionality provided by the xlr-xltestview-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-xltestview-plugin is a XL Release plugin that allows to start a test set on XL TestView.

# Installation #

Starting from version 1.2.0 the version numbering has changed and is now following the versioning from XL TestView.
Any release named `xl-test` is used for any version of XL TestView previous to `1.2.0`.
Any release named `xl-testview` is used for any version of XL TestView `1.2.0+`

## Types ##

+ ExecuteTestSpecification (compatible with XL TestView version 1.2.0)
  * `testSpecificationName`
  * `properties`
+ CheckQualification - Check the latest qualification results from a Test Specification
  * `testSpecificationName`
