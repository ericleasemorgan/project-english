Project English
===============

For the lack of a better name, Project English is an attempt to bring together an estimated 2.5 million English/American works into a single coherent index and accompanying set of natural language processing services. This repository contains the programs and scripts used to make this a reality.

There exists three large collections of English/American literature and published works: Early English Books Online, Eighteenth Century Collection Online, and Sabin Americana. This set of works spans the years 1450 to 1950. It is manifested as a set of XML transcriptions and JPEG page facsimiles. While I have not actually counted how many works are in the proposed collection, I'm guessing there are about 2.5 million items. Taken as a whole, they represent a very large swath of English/American literature. The goal of this Project is to make this whole both accessible & useful to the University of Notre Dame community.

The scripts & programs contained in this repository represent the current technology used to make the goal a reality. Here is an outline of what it contains:

  * __bin__ - the back-end scripts & programs, mostly written in the Bash shell and Perl; these files are used to build the whole thing
  * __cgi-bin__ - a set of programs representing the Web interface to the collection/services; these files are written in Perl and Python
  * __lib__ - a directory for libraries, but since there is only one library, this directory ought to be removed
  * __etc__ - a mishmash of XSL files, SQL templates, CSS stylesheets, Javascript, and templates

_"But where is the beef!?"_ you might say. Well, the raw data XML is not accessible to the general public. It seems as if the data was purchased with strings attached. It is sort of like buying a house in the historical district. You can purchase the house as long as you don't paint it in polka dots. Similarly, I am not allowed to grant access to the resulting index/services for the same licensing restrictions. _Alas._

Software is never done. If it were, then it would be called "hardware", and even now-a-days, such is not even true. Despite these facts, this repository exists for the purposes of code review and transparency. 

For more detail about the why's and wherefore's of Project English, please see the [initial blog posting](http://sites.nd.edu/emorgan/2018/04/project-english/).

---
Eric Lease Morgan \<<emorgan@nd.edu>\>  
May 4, 2018