# tornado-restful

>a simple and extendable way for restful API service on Tornado
>the code support the requests as below for example:

* POST: /item/_id/UPDATE    [UPDATE]
* POST: /item/_id/DELETE    [DELETE]
* POST: /item/NEW           [NEW]
* GET:  /item/LIST          [LIST]
* GET:  /item/?param1=value1&param2=value2&...  [QUERY]
* GET:  /item/_id/resources [FIND_RESOURCE]
* GET:  /item/_id           [FIND_ONE]

>as some of browsers don't support PUT & DELETE well, we use POST for the both.

