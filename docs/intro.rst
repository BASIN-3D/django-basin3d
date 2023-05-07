.. _basin3dintro:

What is Django BASIN-3D?
************************
**Broker for Assimilation, Synthesis and Integration of eNvironmental Diverse, Distributed Datasets**

Django BASIN-3D is a software that synthesizes diverse earth science data from a variety of remote sources in real-time without the need for storing all the data in a single database.
It is a data brokering framework designed to parse, translate, and synthesize diverse observations from well-curated repositories into standardized formats for scientific uses such as analysis and visualization.
Thus, it provides unified access to a diverse set of data sources and data types by connecting
to the providers in real-time and transforming the data streams to provide an integrated view.
BASIN-3D enables users to always have access to the latest data from each of the sources, but to
deal with the data as if all of the data were integrated in local storage.
Importantly users can integrate public data without establishing a prior working relationships with each data source.

Django BASIN-3D is an extendable Python/Django application that uses a generalized data synthesis model that applies across a variety of earth science observation types (hydrology, geochemistry, climate etc.)
The synthesis models, BASIN-3D’s abstracted formats, are based on the Open Geospatial Consortium (OGC) and ISO “Observations and Measurements” (OGC 10-004r3 / ISO 19156: 2013) and OGC “Timeseries Profile of Observations and Measurement “(OGC 15-043r3) data standards.
The synthesized data available via REpresentational State Transfer (REST) Application Programming Interfaces (API).

The current version of  BASIN-3D can be used to integrate time-series earth science observations across a hierarchy of spatial locations.
The use of the OGC/ISO framework makes BASIN-3D extensible to other data types, and in the future we plan to add support for remote sensing and gridded (e.g. model output) data.
BASIN-3D is able to handle multiscale data, through the use of the OGC/ISO framework that allows for specification of hierarchies of spatial features (e.g., points, plots, sites, watersheds, basin).
Thus, users can retrieve data for a specific point location or river basin.

Although Django BASIN-3D is a standalone application, users will need to create a custom broker application on top of BASIN-3D.
The custom broker contains plugins to connect to the specific data sources of interest, and map the data source vocabularies to the BASIN-3D synthesis models.

Readers can find out more about BASIN-3D and its application to the East River Watershed for the Watershed Function SFA at Hubbard et al. (2018), Hendrix et al. (2019), Varadharajan et al. (2022).