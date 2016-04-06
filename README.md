# Preface #

This document describes the functionality provided by the xlr-xltestview-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.


# CI status #

[![Build Status][xlr-xltestview-travis-image] ][xlr-xltestview-travis-url]
[![Codacy Badge][xlr-xltestview-codacy-image] ][xlr-xltestview-codacy-url]
[![Code Climate][xlr-xltestview-code-climate-image] ][xlr-xltestview-code-climate-url]

[xlr-xltestview-travis-image]: https://travis-ci.org/xebialabs-community/xlr-xltestview-plugin.svg?branch=master
[xlr-xltestview-travis-url]: https://travis-ci.org/xebialabs-community/xlr-xltestview-plugin
[xlr-xltestview-codacy-image]: https://api.codacy.com/project/badge/grade/27d1fc3f0d984422b6cde27b84a337d7
[xlr-xltestview-codacy-url]: https://www.codacy.com/app/joris-dewinne/xlr-xltestview-plugin
[xlr-xltestview-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xlr-xltestview-plugin/badges/gpa.svg
[xlr-xltestview-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xlr-xltestview-plugin

# Overview #

The xlr-xltestview-plugin is a XL Release plugin that allows to start a test set on XL TestView.

# Installation #

Starting from version 1.2.0 the version numbering has changed and is now following the versioning from XL TestView.
Any release named `xl-test` is used for any version of XL TestView previous to `1.2.0`.
Any release named `xl-testview` is used for any version of XL TestView `1.2.0+`

Starting from version 1.4.0 you need XLR 4.8.0+ to use the plugin
Starting from version 2.0.0 you also need to specify the `projectName`

## Types ##

+ ExecuteTestSpecification (compatible with XL TestView version 1.4.2+)
  * `testSpecificationName`
  * `projectName`
  * `properties`
+ CheckQualification - Check the latest qualification results from a Test Specification
  * `testSpecificationName`
  * `projectName`
