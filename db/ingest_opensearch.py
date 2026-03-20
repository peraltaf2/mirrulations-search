"""
Ingest dummy data into local OpenSearch matching the real production structure.
Uses separate indices for documents and comments.
"""

from opensearchpy import OpenSearch


def ingest_opensearch():
    """Insert dummy documents and comments into local OpenSearch"""
    
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False,
    )
    
    # Delete indexes
    for index in ["documents", "comments"]:
        if client.indices.exists(index=index):
            client.indices.delete(index=index)
    
    # Create documents index
    client.indices.create(
        index="documents",
        body={
            "mappings": {
                "properties": {
                    "agencyId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "comment": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "docketId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "documentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "documentType": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "modifyDate": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "postedDate": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "title": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    }
                }
            }
        }
    )
    
    # Create comments index
    client.indices.create(
        index="comments",
        body={
            "mappings": {
                "properties": {
                    "commentId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "commentText": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    },
                    "docketId": {
                        "type": "text",
                        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                    }
                }
            }
        }
    )
    
    # Insert documents
    documents = [
        {
            "agencyId": "DEA",
            "comment": "",
            "docketId": "DEA-2024-0059",
            "documentId": "DEA-2024-0059-0001",
            "documentType": "Proposed Rule",
            "modifyDate": "2024-01-15",
            "postedDate": "2024-01-10",
            "title": "This document discusses meaningful use criteria for healthcare"
        },
        {
            "agencyId": "DEA",
            "comment": "",
            "docketId": "DEA-2024-0059",
            "documentId": "DEA-2024-0059-0002",
            "documentType": "Rule",
            "modifyDate": "2024-02-20",
            "postedDate": "2024-02-15",
            "title": "Additional meaningful use requirements and standards"
        },
        {
            "agencyId": "DEA",
            "comment": "Meaningful use standards are important for improving healthcare",
            "docketId": "DEA-2024-0059",
            "documentId": "DEA-2024-0059-0003",
            "documentType": "Rule",
            "modifyDate": "2024-03-10",
            "postedDate": "2024-03-05",
            "title": "Final meaningful use reporting guidelines"
        },
        {
            "agencyId": "CMS",
            "comment": "Medicare updates will help seniors",
            "docketId": "CMS-2025-0240",
            "documentId": "CMS-2025-0240-0001",
            "documentType": "Proposed Rule",
            "modifyDate": "2025-01-20",
            "postedDate": "2025-01-15",
            "title": "Medicare program updates for 2025 including payment changes"
        },
        {
            "agencyId": "CMS",
            "comment": "",
            "docketId": "CMS-2025-0240",
            "documentId": "CMS-2025-0240-0002",
            "documentType": "Rule",
            "modifyDate": "2025-02-10",
            "postedDate": "2025-02-05",
            "title": "Medicare Advantage plan modifications and updates"
        },
    ]
    
    # Insert comments
    comments = [
        {
            "commentId": "DEA-2024-0059-0001",
            "commentText": "I support the meaningful use standards proposed",
            "docketId": "DEA-2024-0059"
        },
        {
            "commentId": "DEA-2024-0059-0002",
            "commentText": "The meaningful use criteria seem reasonable",
            "docketId": "DEA-2024-0059"
        },
        {
            "commentId": "CMS-2025-0240-0001",
            "commentText": "These medicare changes will help seniors",
            "docketId": "CMS-2025-0240"
        },
        {
            "commentId": "CMS-2025-0240-0002",
            "commentText": "I have concerns about medicare funding",
            "docketId": "CMS-2025-0240"
        },
        {
            "commentId": "CMS-2025-0240-0003",
            "commentText": "Medicare should cover more services",
            "docketId": "CMS-2025-0240"
        },
        {
            "commentId": "CMS-2025-0240-0004",
            "commentText": "Support the medicare updates proposed here",
            "docketId": "CMS-2025-0240"
        },
    ]
    
    # Insert documents and comments into OpenSearch
    for doc in documents:
        client.index(
            index="documents",
            id=doc["documentId"],
            body=doc
        )
    
    for comment in comments:
        client.index(
            index="comments",
            id=comment["commentId"],
            body=comment
        )

    client.indices.refresh(index="documents")
    client.indices.refresh(index="comments")

    print(f"✓ Ingested {len(documents)} documents and {len(comments)} comments")
    print("  DEA-2024-0059: 3 docs, 2 comments (term: 'meaningful use')")
    print("  CMS-2025-0240: 2 docs, 4 comments (terms: 'medicare', 'updates')")


if __name__ == "__main__":
    ingest_opensearch()