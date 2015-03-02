exception ValueError {
    1: string message,
}

exception ServerError {
    1: string message,
}

struct collection {
    1: string code
    2: string acronym
    3: string acronym2letters
    4: string status
    5: string domain
}

struct journal_identifiers {
    1: list<string> code,
    2: string collection
}

struct article_identifiers {
    1: string code,
    2: string collection,
    3: string processing_date
}

service ArticleMeta {
    collection get_collection(1: string code) throws (1: ValueError value_err, 2:ServerError server_err),
    string get_article(1: string code, 2: string collection, 3: bool replace_journal_metadata) throws (1: ValueError value_err, 2:ServerError server_err),
    string get_journal(1: string code, 2: string collection) throws (1: ValueError value_err, 2:ServerError server_err),
    list<journal_identifiers> get_journal_identifiers(1: optional string collection, 2: i32 limit, 3: i32 offset) throws (1: ValueError value_err, 2:ServerError server_err),
    list<article_identifiers> get_article_identifiers(1: optional string collection, 2: optional string from, 3: optional string until, 4: i32 limit, 5: i32 offset) throws (1:ValueError value_err, 2:ServerError server_err),
    list<collection> get_collection_identifiers()
}