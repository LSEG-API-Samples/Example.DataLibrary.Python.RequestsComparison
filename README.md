# Comparison of Data Library for Python VS Python/requests direct call for the Delivery Platform (RDP)
- version: 1.0
- Last update: February 2025
- Environment: Windows
- Compiler: Python
- Prerequisite: [Access to RDP credentials](#prerequisite)

## <a id="introduction"></a>Introduction

This project is forked from my old [Comparison of RDP Libraries for Python VS Python/requests direct call for Refinitiv Data Platform](https://github.com/LSEG-API-Samples/Example.RDPLibrary.Python.RequestsComparison) project because the library is outdated. This project aims to use the strategic [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python).

The [Delivery Platform (RDP) APIs](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) (formerly known as Refinitiv Data Platform) provide various LSEG data and content for developers via easy to use Web base API. The developers which are data scientist, financial coder or trader can use any programming languages that support HTTP request-response and JSON message to retrieve content from RDP in a straightforward way. An example use case are data scientists or trader use [Python language](https://www.python.org/) with the [requests library](https://requests.readthedocs.io/en/master/) to get data from RDP and visualize that data in [Jupyter Notebook](https://jupyter.org/) application.

The strategic [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) (aka Data Library version 2) are ease-of-use APIs defining a set of uniform interfaces providing the developer access to the RDP, Real-Time, and Workspace platforms. The libraries let developers can get data easier than using RDP APIs with Python and requests library directly. 

This article demonstrates how easy developers can get LSEG content via Data Library by comparing the application source code using the library ```PlatformSession ``` versus the code using Python/requests to get the same data. The comparison also can be applied to developers who use other Python HTTP libraries such as [http.client](https://docs.python.org/3.7/library/http.client.html#module-http.client) or [urllib.request](https://docs.python.org/3.7/library/urllib.request.html#module-urllib.request).

Note: This article is focusing on **the comparison of how to get data** only. The reason is once the application receives data from either direct RDP APIs call or Data library, the data processing or visualize logic are the same.

## <a id="prerequisite"></a>Demo Applications Prerequisite

This demo project requires the following dependencies.

1. RDP Access credentials.
2. [Python](https://www.python.org/) compiler and runtime.
3. [LSEG Data Library for Python](https://pypi.org/project/lseg-data).
4. Internet connection

Please contact your LSEG's representative to help you to access RDP credentials.

[tbd].
