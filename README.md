# Preface #

This document describes the functionality provided by the xlr-xltestview-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-xltestview-plugin is a XL Release plugin that allows to start a test set on XL TestView.

## Types ##

+ ExecuteTestSpecification (compatible with XL TestView version 0.2.0)
  * `testSpecificationName`
  * `properties`
+ CheckQualification - Check the latest qualification results from a Test Specification
  * 'testSpecificationName`
+ ExecuteLocalTestSet (compatible with XL TestView version 0.1)
  * `testSetDefinition`
  * `testSetType`
+ ExecuteJenkinsTestSet (compatible with XL TestView version 0.1)
  * `testSetDefinition`
  * `jobName`
  * `testSetType`
