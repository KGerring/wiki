curl -X GET "https://toolhub.wikimedia.org/api/tools/?page_size=50" \
 -H "Accept: application/json" \
 -H "X-CSRFToken: 53WbqMZIW22ES7ej29MCOxv

https://toolhub.wikimedia.org/api/tools/?page=2&page_size=50",
 

{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "name": "^[-\\w]+$",
      "title": "AAAAAA",
      "description": "AAAAAA",
      "url": "http://example.com",
      "author": [
        {
          "name": "AAAAAA",
          "wiki_username": "AAAAAA",
          "developer_username": "AAAAAA",
          "email": "user@example.com",
          "url": "http://example.com"
        }
      ],
      "repository": "AAAAAA",
      "subtitle": "AAAAAA",
      "openhub_id": "AAAAAA",
      "url_alternates": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "bot_username": "AAAAAA",
      "deprecated": false,
      "replaced_by": "http://example.com",
      "experimental": false,
      "for_wikis": [
        "^(\\*|(.*)?\\.?(mediawiki|wiktionary|wiki(pedia|quote|books|source|news|versity|data|voyage|media))\\.org)$"
      ],
      "icon": "^https://commons\\.wikimedia\\.org/wiki/File:.+\\..+$",
      "license": "AAAAAA",
      "sponsor": [
        "AAAAAA"
      ],
      "available_ui_languages": [
        "^(x-.*|[A-Za-z]{2,3}(-.*)?)$"
      ],
      "technology_used": [
        "AAAAAA"
      ],
      "tool_type": "web app",
      "api_url": "http://example.com",
      "developer_docs_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "user_docs_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "feedback_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "privacy_policy_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "translate_url": "http://example.com",
      "bugtracker_url": "http://example.com",
      "annotations": {
        "wikidata_qid": "^Q\\d+$",
        "audiences": [
          "admin"
        ],
        "content_types": [
          "article"
        ],
        "tasks": [
          "analysis"
        ],
        "subject_domains": [
          "biography"
        ],
        "deprecated": false,
        "replaced_by": "http://example.com",
        "experimental": false,
        "for_wikis": [
          "^(\\*|(.*)?\\.?(mediawiki|wiktionary|wiki(pedia|quote|books|source|news|versity|data|voyage|media))\\.org)$"
        ],
        "icon": "^https://commons\\.wikimedia\\.org/wiki/File:.+\\..+$",
        "available_ui_languages": [
          "^(x-.*|[A-Za-z]{2,3}(-.*)?)$"
        ],
        "tool_type": "web app",
        "repository": "AAAAAA",
        "api_url": "http://example.com",
        "developer_docs_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "user_docs_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "feedback_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "privacy_policy_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "translate_url": "http://example.com",
        "bugtracker_url": "http://example.com"
      },
      "_schema": "AAAAAA",
      "_language": "AAAAAA",
      "origin": "crawler",
      "created_by": {
        "id": 0,
        "username": "string"
      },
      "created_date": "1970-01-01T00:00:00.000Z",
      "modified_by": {
        "id": 0,
        "username": "string"
      },
      "modified_date": "1970-01-01T00:00:00.000Z"
    }
  ]
}


Single line description
{
count: integer
next: uri┃null
previous: uri┃null
results: [{
name*: string
title*: string
description*: string
url*: uri
keywords: [string]
author: [{
name*: string
wiki_username: string
developer_username: string
email: email
url: uri
}]
repository: string┃null
subtitle: string┃null
openhub_id: string┃null
url_alternates: [{
language: string
url: uri
}]
bot_username: string┃null
deprecated: boolean
replaced_by: uri┃null
experimental: boolean
for_wikis: [string]
icon: string┃null
license: string┃null
sponsor: [string]
available_ui_languages: [string]
technology_used: [string]
tool_type: enum┃null
api_url: uri┃null
developer_docs_url: [{
language: string
url: uri
}]
user_docs_url: [{
language: string
url: uri
}]
feedback_url: [{
language: string
url: uri
}]
privacy_policy_url: [{
language: string
url: uri
}]
translate_url: uri┃null
bugtracker_url: uri┃null
annotations: {
wikidata_qid: string┃null
audiences: [enum]
content_types: [enum]
tasks: [enum]
subject_domains: [enum]
deprecated: boolean
replaced_by: uri┃null
experimental: boolean
for_wikis: [string]
icon: string┃null
available_ui_languages: [string]
tool_type: enum┃null
repository: string┃null
api_url: uri┃null
developer_docs_url: [{
language: string
url: uri
}]
user_docs_url: [{
language: string
url: uri
}]
feedback_url: [{
language: string
url: uri
}]
privacy_policy_url: [{
language: string
url: uri
}]
translate_url: uri┃null
bugtracker_url: uri┃null
}
_schema: string┃null
_language: string┃null
origin: enum
created_by: {
id: integer 🆁
username: string 🆁
}
created_date: date-time 🆁
modified_by: {
id: integer 🆁
username: string 🆁
}
modified_date: date-time 🆁
}]
}

'''json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "facets": {},
  "results": [
    {
      "name": "string",
      "title": "string",
      "description": "string",
      "url": "string",
      "author": [
        {
          "name": "AAAAAA",
          "wiki_username": "AAAAAA",
          "developer_username": "AAAAAA",
          "email": "user@example.com",
          "url": "http://example.com"
        }
      ],
      "repository": "string",
      "subtitle": "string",
      "openhub_id": "string",
      "url_alternates": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "bot_username": "string",
      "deprecated": false,
      "replaced_by": "string",
      "experimental": false,
      "for_wikis": [
        "^(\\*|(.*)?\\.?(mediawiki|wiktionary|wiki(pedia|quote|books|source|news|versity|data|voyage|media))\\.org)$"
      ],
      "icon": "string",
      "license": "string",
      "sponsor": [
        "AAAAAA"
      ],
      "available_ui_languages": [
        "^(x-.*|[A-Za-z]{2,3}(-.*)?)$"
      ],
      "technology_used": [
        "AAAAAA"
      ],
      "tool_type": "string",
      "api_url": "string",
      "developer_docs_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "user_docs_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "feedback_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "privacy_policy_url": [
        {
          "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
          "url": "http://example.com"
        }
      ],
      "translate_url": "string",
      "bugtracker_url": "string",
      "annotations": {
        "wikidata_qid": "^Q\\d+$",
        "audiences": [
          "admin"
        ],
        "content_types": [
          "article"
        ],
        "tasks": [
          "analysis"
        ],
        "subject_domains": [
          "biography"
        ],
        "deprecated": false,
        "replaced_by": "http://example.com",
        "experimental": false,
        "for_wikis": [
          "^(\\*|(.*)?\\.?(mediawiki|wiktionary|wiki(pedia|quote|books|source|news|versity|data|voyage|media))\\.org)$"
        ],
        "icon": "^https://commons\\.wikimedia\\.org/wiki/File:.+\\..+$",
        "available_ui_languages": [
          "^(x-.*|[A-Za-z]{2,3}(-.*)?)$"
        ],
        "tool_type": "web app",
        "repository": "AAAAAA",
        "api_url": "http://example.com",
        "developer_docs_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "user_docs_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "feedback_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "privacy_policy_url": [
          {
            "language": "^(x-.*|[A-Za-z]{2,3}(-.*)?)$",
            "url": "http://example.com"
          }
        ],
        "translate_url": "http://example.com",
        "bugtracker_url": "http://example.com"
      },
      "_schema": "string",
      "_language": "string",
      "origin": "string",
      "created_by": {
        "id": 0,
        "username": "string"
      },
      "created_date": "1970-01-01",
      "modified_by": {
        "id": 0,
        "username": "string"
      },
      "modified_date": "1970-01-01"
    }
  ]
}'''
